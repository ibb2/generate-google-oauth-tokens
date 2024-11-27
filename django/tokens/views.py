import os

import requests
from dotenv import load_dotenv

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import TokenSerializer

# load env
load_dotenv()

# Create your views here.


@api_view(["POST"])
def generate_oauth_tokens(request):
    """
    Generate OAuth tokens using the provided authorization code.

    This function exchanges the authorization code for access, refresh, and ID tokens,
    following the OAuth 2.0 protocol. For details, refer to:
    https://developers.google.com/identity/protocols/oauth2/native-app#exchange-authorization-code

    Parameters
    ----------
    request : Request
        The request object containing the following required attributes:
            - code (str): The authorization code obtained from the initial OAuth authorization request.
            - client_id (str): Your application's Google OAuth Client ID.
            - client_secret (str): Your application's Google OAuth Client Secret.
            - redirect_uri (str): The redirect URI, which must match the one specified in the Google OAuth configuration.
            - grant_type (str): The grant type, which must be set to "authorization_code".

    Returns
    -------
    response : Response
        A response object containing the following attributes:
            - access_token (str): The token that grants access to protected resources.
            - id_token (str): A token that contains user identity information.
            - refresh_token (str, optional): A token used to obtain a new access token when the current one expires.
            - expires_in (int): The remaining lifetime of the access token in seconds.
            - scope (str): The scopes associated with the granted access token.

    Raises
    ------
    OAuthException
        If the authorization code exchange fails, this exception is raised with details about the error.
    """

    if request.method == "GET":
        return Response("Please use POST request", status = 301)

    if request.method == "POST":
        print(f'Request data {request.data}')
        serializer = TokenSerializer(data = request.data)
        if serializer.is_valid():

            try:
                code = serializer.data['code']
                print(f'code: {code}')

                # Setting payload
                payload = {
                    "code": code, # Authorization code
                    "client_id": os.environ.get("GOOGLE_CLIENT_ID"), # Google OAuth Client ID
                    "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET"), # Google OAuth Client Secret
                    "redirect_uri": os.environ.get("REDIRECT_URI"), # Redirect URI, has to match Google OAuth Redirect URI
                    "grant_type": os.environ.get("GRANT_TYPE") # Grant type (always authorization_code)
                }

                # Making request to Google token endpoint, as defined in the OAuth 2.0 specification
                r = requests.post("https://oauth2.googleapis.com/token", payload)

                match r.status_code:
                    # Handling response
                    case range(200, 299):
                        return Response(r.json(), status = r.status_code)
                    # Handling errors
                    case 400:
                        return Response(r.json(), status = 400)
                    case 401:
                        return Response(r.json(), status = 401)
                    case 403:
                        return Response(r.json(), status = 403)
                    case 404:
                        return Response(r.json(), status = 404)
                    case 500:
                        return Response(r.json(), status = 500)
                    case _:
                        return Response(r.json(), status = r.status_code)

            except ConnectionError as E:
                return Response(E, status = 503)

        return Response("Invalid data", status = 400)