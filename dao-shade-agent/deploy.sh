#!/bin/bash

# ====== Shade Agent TEE Deployment ======
# Strictly for production-ready TEE deployment per NEAR's requirements

# 1. REQUIRED PRECONDITIONS
echo "🔵 VERIFYING PREREQUISITES..."
command -v docker >/dev/null 2>&1 || { 
    echo >&2 "❌ Docker not found. Install it first: https://docs.docker.com/engine/install/";
    exit 1;
}
near --version >/dev/null 2>&1 || { 
    echo >&2 "❌ NEAR CLI not found. Run: npm install -g near-cli";
    exit 1;
}

# 2. ENVIRONMENT SETUP
export NEAR_ENV=testnet
export CONTRACT_NAME="dao-reviewer-agent.$(near whoami | awk '{print $1}')"
echo "🆔 Contract will be deployed as: $CONTRACT_NAME"

# 3. SHADE AGENT SETUP
echo "🔵 INSTALLING SHADE AGENT CLI..."
npm install -g @neardefi/shade-agent-cli

# 4. BUILD TEE-COMPATIBLE IMAGE
echo "🔵 BUILDING DOCKER IMAGE FOR TEE..."
docker build -t dao-reviewer-tee-image .

# 5. DEPLOY TO TESTNET
echo "🔵 DEPLOYING CONTRACT..."
shade-agent-cli deploy \
  --network testnet \
  --contract-name $CONTRACT_NAME \
  --wasm-path ./contract/shade_agent.wasm || {
    echo >&2 "❌ Deployment failed. Ensure:";
    echo >&2 " - You have testnet tokens (near login)";
    echo >&2 " - ./contract/shade_agent.wasm exists";
    exit 1;
}

# 6. LAUNCH IN TEE
echo "🔵 STARTING TEE EXECUTION..."
shade-agent-cli run \
  --image dao-reviewer-tee-image \
  --network testnet \
  --contract $CONTRACT_NAME

# 7. VERIFICATION
echo "✅ TEE DEPLOYMENT SUCCESSFUL!"
echo "🌐 Access your agent at: http://localhost:5000"
echo "📜 Contract ID: $CONTRACT_NAME"