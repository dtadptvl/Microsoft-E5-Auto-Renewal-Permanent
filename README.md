# Microsoft E5 Auto Renew (The Easy Way)

G'day! Welcome to the simplest way to keep your Microsoft Developer E5 subscription alive.

This script runs on GitHub Actions. It randomly pings Microsoft Graph APIs to show you are actively using the account. The best part is we use a Public Client setup. This means you do not have to worry about updating a Client Secret every two years. 

## ⚠️ The Catch (Risks & Blind Spots)
Before you jump in, you need to know the risks.
*   **The "Impossible Travel" Flag:** GitHub Actions runs on servers all over the world. Your setup will look like it is teleporting across the globe every few hours. Microsoft might lock the account if their security gets suspicious.
*   **GitHub Ban Hammer:** Running a script too often on free GitHub Actions can flag your repo for abuse. Stick to the default schedule to stay under the radar.
*   **No Guarantees:** Microsoft's renewal algorithm is a black box. This tool boosts your chances but it is not a 100% magic bullet.

## 🛠️ Step 1: Set Up Azure
First, we need to register an app in Microsoft Azure.
1. Go to the Azure Portal and search for **Microsoft Entra ID** (formerly Azure Active Directory).
2. Click on **App registrations**, then click **New registration**.
3. Give it a name like `E5 Renew App`.
4. Leave the rest as default and click **Register**.
5. On the left menu, click **Authentication**.
6. Click **Add a platform** and choose **Mobile and desktop applications**.
7. In the Custom redirect URIs box, type exactly `http://localhost`.
8. Tick the box for `https://login.microsoftonline.com/common/oauth2/nativeclient`.
9. Hit **Save**.
10. Go to the **Overview** page and copy your **Application (client) ID**. You will need this later.

## 🔑 Step 2: Get Your First Token
Since we do not use a secret, we need to authorize the app manually the first time.
1. Download the `get_token.py` file to your computer.
2. Open it in a text editor and paste your Client ID where it says `NHẬP_CLIENT_ID_CỦA_BẠN_VÀO_ĐÂY`.
3. Run the script using Python in your terminal: `python get_token.py`
4. The script will give you a code and a link. Open the link in your browser, enter the code, and log in with your E5 Admin account.
5. Head back to your terminal. It will print out a long **Refresh Token**. Copy this and keep it safe.

## ⚙️ Step 3: Set Up GitHub Secrets
Now we hand the keys over to GitHub Actions.
1. Go to your GitHub repository.
2. Click on **Settings**, expand **Secrets and variables**, and click **Actions**.
3. You need to create three **New repository secrets**:
    *   `CLIENT_ID`: Paste the Application ID from Step 1.
    *   `REFRESH_TOKEN`: Paste the token you got in Step 2.
    *   `GH_TOKEN`: This is your GitHub Personal Access Token. You need to generate this in your GitHub account settings (Developer settings > Personal access tokens > Tokens (classic)). Make sure you give it the `repo` permission so it can update the token automatically.

## 🚀 Step 4: Let It Run!
That is it! You just need the `auto_renew.py` and `.github/workflows/renew.yml` files in your repo.

The GitHub Action is set to run a few times a day. It will grab a fresh token, update your GitHub Secrets automatically, and ping a few random APIs. 

Sit back, relax, and let the code do the heavy lifting!
