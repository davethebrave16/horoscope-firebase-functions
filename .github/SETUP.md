# GitHub Actions Setup

This project includes automated CI/CD workflows for testing and deployment.

## 🔧 Required Secrets

To enable deployment, add these secrets to your GitHub repository:

### 1. Firebase Token
- **Secret Name**: `FIREBASE_TOKEN`
- **How to get**: Run `firebase login:ci` locally
- **Value**: The token returned by the command

### 2. API Key
- **Secret Name**: `API_KEY`
- **Value**: Your API key for Firebase Functions authentication
- **Required**: Yes - Functions need this for authorization

## 📋 Workflows

### `pr-test.yml` - Pull Request Tests
- **Triggers**: On pull requests to master/main
- **Actions**: Runs tests with coverage
- **Purpose**: Ensure code quality before merging

### `test.yml` - Push Tests  
- **Triggers**: On push to master/main
- **Actions**: Runs tests with coverage
- **Purpose**: Continuous testing

### `deploy.yml` - Deployment
- **Triggers**: On push to master/main
- **Actions**: Runs tests + deploys to Firebase
- **Purpose**: Automated deployment

## 🚀 Setup Steps

1. **Add Firebase Token**:
   ```bash
   firebase login:ci
   # Copy the token and add it as FIREBASE_TOKEN secret
   ```

2. **Enable GitHub Actions**:
   - Go to repository Settings → Actions
   - Enable "Allow all actions and reusable workflows"

3. **Test the workflows**:
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
