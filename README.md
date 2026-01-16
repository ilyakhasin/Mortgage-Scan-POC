# Mortgage Scan POC - Veryfi OCR Integration

A minimal Expo-managed React Native proof-of-concept that uses Veryfi OCR to extract mortgage fields from document photos.

## 🎯 Overview

This POC provides a single-screen mobile app that:
- Lets users take a photo of a mortgage statement
- Uploads the image to Veryfi OCR service
- Displays extracted core mortgage fields in a simple table

**⚠️ Note:** This is a proof-of-concept implementation. The VERYFI_API_KEY is embedded at build time for demonstration purposes. Production apps should use secure backend API proxies instead of embedding API keys in the APK.

## 📋 Prerequisites

- Node.js 20+
- Android device or emulator for testing
- Veryfi API Key ([Get one here](https://www.veryfi.com/))

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/ilyakhasin/Mortgage-Scan-POC.git
cd Mortgage-Scan-POC
```

### 2. Install dependencies
```bash
cd mobile
npm install
```

### 3. Set up Veryfi API Key

For local development, set the environment variable:
```bash
export VERYFI_API_KEY="your_api_key_here"
```

### 4. Run the app
```bash
npm start
```

Then press 'a' to open on Android, or scan the QR code with Expo Go app.

## 🏗️ CI/CD - Building Android APK

This repository includes a GitHub Actions workflow that automatically builds an Android debug APK.

### Setting up the VERYFI_API_KEY Secret

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `VERYFI_API_KEY`
5. Value: Your Veryfi API key
6. Click **Add secret**

### Downloading the APK

1. Go to **Actions** tab in your GitHub repository
2. Click on the latest workflow run (triggered by push to main or PR)
3. Scroll down to **Artifacts** section
4. Download **android-debug-apk**
5. Extract the zip file to get `app-debug.apk`
6. Install on your Android device:
   ```bash
   adb install app-debug.apk
   ```

### Manual Workflow Trigger

You can also manually trigger the build:
1. Go to **Actions** tab
2. Select **Android Build** workflow
3. Click **Run workflow**
4. Select branch and click **Run workflow**

## 📱 How to Use the App

1. Open the app on your Android device
2. Tap **"Take Picture"** button
3. Grant camera permissions when prompted
4. Point camera at a mortgage statement
5. Tap **"Capture"** to take the photo
6. Wait while the image is uploaded and processed
7. View the extracted fields in the table:
   - Borrower name
   - Loan number
   - Property address
   - Statement date
   - Due date
   - Current principal balance
   - Interest rate
   - Monthly payment
   - Servicer name
   - Account number

## 🏗️ Architecture

### File Structure
```
mobile/
├── App.js                    # Main application component
├── src/
│   └── veryfiClient.js      # Veryfi API wrapper and field mapping
├── package.json             # Dependencies
└── app.json                 # Expo configuration

.github/
└── workflows/
    └── android-build.yml    # CI workflow for building APK
```

### Core Components

**App.js**: Single-screen React component with:
- Camera UI using expo-camera
- Image capture and upload logic
- Results display table
- Error handling and loading states

**veryfiClient.js**: API wrapper that:
- Uploads images to Veryfi Documents endpoint
- Maps Veryfi response to 10 canonical mortgage fields
- Handles authentication via API key header

## 🔒 Security Note

**⚠️ Important:** This POC embeds the VERYFI_API_KEY at build time for demonstration purposes. In production:
- Use a secure backend API to proxy Veryfi requests
- Never embed API keys directly in mobile apps
- Implement proper authentication and rate limiting
- Use environment-specific configurations

## 📝 Extracted Fields

The app extracts and displays these 10 core mortgage fields:

1. **Borrower name** - Name of the loan borrower
2. **Loan number** - Unique loan identifier
3. **Property address** - Address of the mortgaged property
4. **Statement date** - Date the statement was issued
5. **Due date** - Next payment due date
6. **Current principal balance** - Outstanding loan balance
7. **Interest rate** - Current interest rate
8. **Monthly payment** - Required monthly payment amount
9. **Servicer name** - Name of the loan servicer
10. **Account number** - Account/reference number

## 🛠️ Development

### Running locally
```bash
cd mobile
npm start
```

### Building for Android
```bash
cd mobile
npx expo prebuild --platform android
cd android
./gradlew assembleDebug
```

The APK will be at: `android/app/build/outputs/apk/debug/app-debug.apk`

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

This is a proof-of-concept project. For production use, consider:
- Implementing secure backend API proxy
- Adding comprehensive error handling
- Supporting iOS platform
- Adding field validation and editing
- Implementing offline support
- Adding multi-document batch processing

## 📞 Support

For Veryfi API questions, visit: https://docs.veryfi.com/
For issues with this POC, open a GitHub issue.
