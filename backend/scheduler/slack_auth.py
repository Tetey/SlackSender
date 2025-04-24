"""
Slack authentication utilities
"""
import logging
import os
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from slack_sdk.oauth import AuthorizeUrlGenerator
from slack_sdk.oauth.installation_store import FileInstallationStore
from slack_sdk.oauth.state_store import FileOAuthStateStore

logger = logging.getLogger(__name__)

# Create installation store and state store directories
os.makedirs('slack_installation', exist_ok=True)
os.makedirs('slack_state', exist_ok=True)

# Initialize installation store and state store
installation_store = FileInstallationStore(base_dir='slack_installation')
state_store = FileOAuthStateStore(expiration_seconds=300, base_dir='slack_state')

# Use ngrok URL for Slack OAuth
NGROK_URL = "https://cb4b-124-217-62-119.ngrok-free.app"

def get_authorize_url(request):
    """
    Generate a Slack OAuth authorization URL
    """
    # Use ngrok URL for redirect in development
    redirect_uri = f"{NGROK_URL}/api/slack/oauth-callback/"
    
    authorize_url_generator = AuthorizeUrlGenerator(
        client_id=settings.SLACK_CLIENT_ID,
        scopes=["chat:write", "channels:read", "groups:read"],
        redirect_uri=redirect_uri,
    )
    
    # Generate a state parameter for CSRF protection
    state = state_store.issue()
    
    # Generate the authorization URL
    authorize_url = authorize_url_generator.generate(state)
    
    return authorize_url, state

def handle_oauth_callback(request):
    """
    Handle the OAuth callback from Slack
    """
    from slack_sdk.oauth.installation_store.models.installation import Installation
    
    code = request.GET.get('code')
    state = request.GET.get('state')
    
    # Verify the state parameter to prevent CSRF attacks
    if not state_store.consume(state):
        logger.error("Invalid OAuth state parameter")
        return HttpResponseRedirect(reverse('slack_auth_error'))
    
    if not code:
        logger.error("No authorization code provided")
        return HttpResponseRedirect(reverse('slack_auth_error'))
    
    # Exchange the authorization code for an access token
    from slack_sdk.web.client import WebClient
    client = WebClient()
    
    try:
        # Use ngrok URL for redirect in development
        redirect_uri = f"{NGROK_URL}/api/slack/oauth-callback/"
        
        # Complete the OAuth flow
        oauth_response = client.oauth_v2_access(
            client_id=settings.SLACK_CLIENT_ID,
            client_secret=settings.SLACK_CLIENT_SECRET,
            code=code,
            redirect_uri=redirect_uri,
        )
        
        # Log the full OAuth response for debugging
        logger.info(f"OAuth response: {oauth_response}")
        
        # Extract the refresh token if available
        refresh_token = oauth_response.get("refresh_token", "")
        if refresh_token:
            # In a production environment, you would securely store this
            # For now, we'll log it (not recommended for production)
            logger.info(f"Received refresh token: {refresh_token}")
            
            # You might want to update your .env file or store in a secure database
            # For this example, we'll just use the one from settings
        
        # Save the installation
        installation = Installation(
            app_id=oauth_response.get("app_id"),
            enterprise_id=oauth_response.get("enterprise_id"),
            team_id=oauth_response.get("team_id"),
            bot_token=oauth_response.get("access_token"),
            bot_id=oauth_response.get("bot_user_id"),
            bot_user_id=oauth_response.get("bot_user_id"),
            bot_scopes=oauth_response.get("scope", "").split(","),
            user_id=oauth_response.get("authed_user", {}).get("id"),
            user_token=oauth_response.get("authed_user", {}).get("access_token"),
            user_scopes=oauth_response.get("authed_user", {}).get("scope", "").split(","),
            installed_at=oauth_response.get("installer_user_id"),
            # Store the refresh token in the installation
            user_refresh_token=refresh_token,
        )
        installation_store.save(installation)
        
        return HttpResponseRedirect(reverse('slack_auth_success'))
    
    except Exception as e:
        logger.error(f"Error during OAuth flow: {e}")
        return HttpResponseRedirect(reverse('slack_auth_error'))
