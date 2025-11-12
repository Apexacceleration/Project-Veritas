# New Streamlit Secrets Format (Native OIDC)

**We've switched to Streamlit's native OAuth support - much more reliable!**

---

## Replace Your Entire Streamlit Secrets With This:

```toml
# OpenAI API Key
OPENAI_API_KEY = "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"

# Whitelisted Emails (comma-separated, no spaces)
ALLOWED_EMAILS = "tyler@apexacceleration.com,tdavidson525@gmail.com,ttermei@gmail.com"

# Google OAuth Configuration (Streamlit Native OIDC)
[auth]
client_id = "YOUR_CLIENT_ID_HERE.apps.googleusercontent.com"
client_secret = "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"
redirect_uri = "https://project-veritas.streamlit.app/oauth2callback"
cookie_secret = "veritas-cookie-secret-random-string-12345"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"
```

---

## What Changed:

### Old Format (Broken):
```toml
GOOGLE_CLIENT_ID = "..."
GOOGLE_CLIENT_SECRET = "..."
redirect_uri = "..."
```

### New Format (Native Streamlit OIDC):
```toml
[auth]
client_id = "..."
client_secret = "..."
redirect_uri = "...oauth2callback"
cookie_secret = "..."
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"
```

---

## Key Differences:

1. **`[auth]` section** - Groups OAuth config together
2. **`redirect_uri` ends with `/oauth2callback`** - Required by Streamlit's OIDC
3. **`cookie_secret`** - Random string for session security
4. **`server_metadata_url`** - Points to Google's OIDC discovery endpoint

---

## Update Your Google Cloud Console Redirect URI:

**IMPORTANT:** You need to update the redirect URI in Google Cloud Console!

1. Go to: [console.cloud.google.com/apis/credentials](https://console.cloud.google.com/apis/credentials)
2. Click on your OAuth client
3. Under **"Authorized redirect URIs"**, **ADD** this new one:
   ```
   https://project-veritas.streamlit.app/oauth2callback
   ```
   ⚠️ **Notice the `/oauth2callback` at the end!**

4. Keep your old one too (won't hurt):
   ```
   https://project-veritas.streamlit.app
   ```

5. Click **"Save"**

---

## Copy/Paste This Into Streamlit Secrets:

```toml
OPENAI_API_KEY = "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"

ALLOWED_EMAILS = "tyler@apexacceleration.com,tdavidson525@gmail.com,ttermei@gmail.com"

[auth]
client_id = "YOUR_CLIENT_ID_HERE.apps.googleusercontent.com"
client_secret = "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"
redirect_uri = "https://project-veritas.streamlit.app/oauth2callback"
cookie_secret = "veritas-cookie-secret-random-string-12345"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"
```

**Replace `YOUR_CLIENT_ID_HERE` with your actual Client ID!**

---

## Why This Fixes Everything:

✅ **Native Streamlit support** - No buggy third-party libraries
✅ **Officially maintained** - Streamlit team keeps it updated
✅ **More reliable** - No more `invalid_grant` errors
✅ **Simpler code** - Uses `st.login()` and `st.logout()`
✅ **Better UX** - Smoother login flow

---

**After updating secrets, the app will redeploy and OAuth will work properly!**
