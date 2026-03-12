# ⚡ POWER MODZ OTP BOT ⚡

Complete OTP forwarding bot with Admin Panel for Railway.app deployment.

## 🚀 Features

- ⚡ Power Modz message format
- 🔘 4 customizable buttons (2x2 grid)
- 👑 Full admin panel with `/start` command
- 📨 Enable/Disable OTP sending in real-time
- 🔧 Edit button text and URLs on-the-fly
- 📊 Live statistics and monitoring
- 🧵 Multi-threaded for optimal performance

## 📋 Admin Panel Features

### Main Menu
- 📨 Manage OTPs
- 🔘 Manage Buttons
- 👑 Owner Panel

### OTP Management
- ✅ Enable OTP sending
- ❌ Disable OTP sending
- 📊 Check current status

### Button Management
- Edit all 4 buttons
- Change text and URLs
- Live updates

### Owner Panel
- View statistics
- Bot information
- Processed message count

## 🌐 Deploy to Railway.app

### Step 1: Fork/Upload to GitHub
1. Create a new repository on GitHub
2. Upload all files from this ZIP
3. Commit and push

### Step 2: Deploy on Railway
1. Go to [Railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Railway will auto-detect and deploy!

### Step 3: Set Environment Variables
In Railway dashboard, add these variables:

```
TELEGRAM_BOT_TOKEN=8430484880:AAEDwu_Rf6-E25d4DdCSOYTqvEhcoCf8ga0
TELEGRAM_CHANNEL_ID=-1003852492977
OWNER_ID=8290661165
API_URL=http://147.135.212.197/crapi/st/viewstats
API_TOKEN=R1BTQ0hBUzSAild8c2aWV3eYa1NpjVNIUpBzY1qCaWFHh5JUUpWIXQ==
CHECK_INTERVAL=15
BATCH_SIZE=50
MAX_RECORDS_PER_FETCH=1000000000
```

### Step 4: Access Admin Panel
1. Find your bot on Telegram
2. Send `/start` command
3. Admin panel will open!

## 📱 Usage

### For Users (In Channel)
OTPs will be automatically posted with:
- Time, Country, Service, Number
- OTP code highlighted
- Full message text
- 4 custom buttons

### For Admin (In Bot DM)
Send `/start` to access:
- Real-time OTP control
- Button customization
- Statistics and monitoring

## 🔧 Configuration

### Your Current Settings
- **Bot Token:** `8430484880:AAEDwu_Rf6-E25d4DdCSOYTqvEhcoCf8ga0`
- **Channel ID:** `-1003852492977`
- **Owner ID:** `8290661165`
- **Check Interval:** 15 seconds
- **Batch Size:** 50 messages

### Button Configuration
Edit in `main.py` or via admin panel:
```python
BUTTON_CONFIG = {
    "btn1": {"text": "☎️ NUMBERS", "url": "https://t.me/dp_numbers"},
    "btn2": {"text": "😈 DEVELOPER", "url": "https://t.me/powermodzzz"},
    "btn3": {"text": "📁 FOLDER", "url": "https://t.me/addlist/j1oWFpRCPE9mNmFk"},
    "btn4": {"text": "🟢 WhatsApp", "url": "https://whatsapp.com/channel/0029Vb6oQ4CIN9ip6RfTmT0c"}
}
```

## 📊 Message Format

```
✨    NEW OTP RECEIVED    ✨
━━━━━━━━━━━━━━━━━━━━━━━━━━
🕐 Time: 2026-02-16 03:28:14
🇿🇼 Country: Zimbabwe
🟢 Service: WhatsApp
📞 Number: +2637****775
🔑 OTP: 135-346
━━━━━━━━━━━━━━━━━━━━━━━━━━
📧 Full Message:
[complete SMS text]
━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ Powered By Power Modz ⚡

[Button1] [Button2]
[Button3] [Button4]
```

## 🛠️ Troubleshooting

### Bot not responding to /start
- Check OWNER_ID is correct
- Verify bot token is valid
- Check Railway logs

### OTPs not being sent
- Use admin panel to enable OTP sending
- Check API_URL is accessible
- Verify channel ID is correct (with `-` prefix)

### Buttons not showing
- Check button URLs are valid
- Verify BUTTON_CONFIG in code
- Test with admin panel editing

## 📝 Files Included

- `main.py` - Main bot script
- `requirements.txt` - Python dependencies
- `Procfile` - Railway start command
- `runtime.txt` - Python version
- `.env.example` - Environment variables template
- `README.md` - This file

## 🔒 Security Notes

- Never commit `.env` file to GitHub
- Keep bot token private
- Owner ID restricts admin access
- Use environment variables on Railway

## 💡 Tips

1. **Test locally first:**
   ```bash
   pip install -r requirements.txt
   python main.py
   ```

2. **Monitor Railway logs:**
   - Check for errors
   - View OTP sending activity
   - Monitor API calls

3. **Use admin panel:**
   - Disable during maintenance
   - Edit buttons without redeployment
   - Check statistics regularly

## 📞 Support

Created by **Power Modz** ⚡

For issues or questions:
- Developer: [@powermodzzz](https://t.me/powermodzzz)
- Channel: [Power Modz Channel](https://t.me/dp_numbers)

## ⚡ Power Modz - Best OTP Bot ⚡
