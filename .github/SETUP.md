# GitHub Actions Setup

This project includes automated CI/CD workflows for testing and deployment.

## 🔧 Required Secrets

To enable deployment, add these secrets to your GitHub repository:

### 1. Firebase Token
- **Secret Name**: `FIREBASE_TOKEN`
- **How to get**: Run `firebase login:ci` locally
- **Value**: The token returned by the command

### 2. Firebase Project ID
- **Secret Name**: `FIREBASE_PROJECT_ID`
- **How to get**: From Firebase Console or `firebase projects:list`
- **Value**: Your Firebase project ID (e.g., `my-project-12345`)

### 3. API Key
- **Secret Name**: `API_KEY`
- **Value**: Your API key for Firebase Functions authentication
- **Required**: Yes - Functions need this for authorization

## 📋 Workflows

### `test.yml` - Pull Request Tests
- **Triggers**: On pull requests to master/main
- **Actions**: Runs tests with coverage
- **Purpose**: Ensure code quality before merging

### `deploy.yml` - Deployment
- **Triggers**: On push to master/main
- **Actions**: Runs tests + deploys to Firebase
- **Purpose**: Automated deployment

## 🚀 Setup Steps

1. **Get Firebase Token**:
   ```bash
   firebase login:ci
   # Copy the token and add it as FIREBASE_TOKEN secret
   ```

2. **Get Firebase Project ID**:
   ```bash
   firebase projects:list
   # Copy your project ID and add it as FIREBASE_PROJECT_ID secret
   ```

3. **Add GitHub Secrets**:
   - Go to repository Settings → Secrets and variables → Actions
   - Add `FIREBASE_TOKEN` with the token from step 1
   - Add `FIREBASE_PROJECT_ID` with your project ID from step 2
   - Add `API_KEY` with your API key

4. **Enable GitHub Actions**:
   - Go to repository Settings → Actions
   - Enable "Allow all actions and reusable workflows"

5. **Test the workflows**:
   - Create a test branch
   - Make a small change
   - Create a PR to see tests run

## 📊 Coverage Reports

- Tests run with coverage reporting
- Coverage threshold: 80% (configurable)
- Reports available in Actions tab
- XML coverage file generated for integration

## 🔍 Monitoring

- Check Actions tab for workflow status
- Tests must pass before deployment
- Deployment only happens on master/main branch
- All functions maintain API compatibility
