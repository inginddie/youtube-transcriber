#!/bin/bash
# Helper script para deployment de YouTube Transcriber Pro

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Main menu
show_menu() {
    clear
    print_header "YouTube Transcriber Pro - Deploy Helper"
    echo ""
    echo "1) Generate secure ACCESS_CODE"
    echo "2) Validate environment variables"
    echo "3) Test security integration"
    echo "4) Merge to main and push"
    echo "5) Show Railway environment variables template"
    echo "6) Run syntax checks"
    echo "7) Exit"
    echo ""
    read -p "Select option: " choice

    case $choice in
        1) generate_access_code ;;
        2) validate_env ;;
        3) test_security ;;
        4) merge_and_push ;;
        5) show_env_template ;;
        6) syntax_check ;;
        7) exit 0 ;;
        *) print_error "Invalid option"; sleep 2; show_menu ;;
    esac
}

generate_access_code() {
    print_header "Generate Secure ACCESS_CODE"

    if command -v python3 &> /dev/null; then
        echo "Generating 32-byte URL-safe token..."
        echo ""
        ACCESS_CODE=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
        print_success "Your new ACCESS_CODE:"
        echo ""
        echo -e "${GREEN}${ACCESS_CODE}${NC}"
        echo ""
        echo "Length: ${#ACCESS_CODE} characters"
        echo ""
        echo "Copy this code and set it in:"
        echo "  - Railway Dashboard > Variables > ACCESS_CODE"
        echo "  - Or in your .env file for local testing"
        echo ""
    else
        print_error "Python3 not found. Please install Python3."
    fi

    read -p "Press Enter to continue..."
    show_menu
}

validate_env() {
    print_header "Validate Environment Variables"

    if [ -f ".env" ]; then
        print_success ".env file found"
        echo ""

        # Check required variables
        required_vars=("OPENAI_API_KEY")
        security_vars=("REQUIRE_AUTH" "ACCESS_CODE" "MAX_TRANSCRIPTIONS_PER_HOUR" "MAX_SEARCHES_PER_MINUTE" "MAX_CHATS_PER_MINUTE")

        echo "Required Variables:"
        for var in "${required_vars[@]}"; do
            if grep -q "^${var}=" .env; then
                value=$(grep "^${var}=" .env | cut -d'=' -f2)
                if [ -n "$value" ]; then
                    print_success "$var is set"
                else
                    print_warning "$var is empty"
                fi
            else
                print_error "$var is missing"
            fi
        done

        echo ""
        echo "Security Variables:"
        for var in "${security_vars[@]}"; do
            if grep -q "^${var}=" .env; then
                value=$(grep "^${var}=" .env | cut -d'=' -f2)
                if [ -n "$value" ]; then
                    print_success "$var = $value"
                else
                    print_warning "$var is empty (using default)"
                fi
            else
                print_warning "$var not set (using default)"
            fi
        done

    else
        print_warning ".env file not found"
        echo ""
        echo "Would you like to create one from .env.example?"
        read -p "(y/n): " create_env

        if [ "$create_env" = "y" ]; then
            cp .env.example .env
            print_success ".env created from .env.example"
            echo "Please edit .env and add your API keys"
        fi
    fi

    echo ""
    read -p "Press Enter to continue..."
    show_menu
}

test_security() {
    print_header "Test Security Integration"

    if [ -f "test_security_integration.py" ]; then
        echo "Running security integration tests..."
        echo ""

        if command -v python3 &> /dev/null; then
            python3 test_security_integration.py
            echo ""
        else
            print_error "Python3 not found"
        fi
    else
        print_error "test_security_integration.py not found"
    fi

    read -p "Press Enter to continue..."
    show_menu
}

merge_and_push() {
    print_header "Merge to Main and Push"

    # Check current branch
    current_branch=$(git branch --show-current)
    echo "Current branch: $current_branch"
    echo ""

    # Check for uncommitted changes
    if ! git diff-index --quiet HEAD --; then
        print_error "You have uncommitted changes!"
        git status --short
        echo ""
        read -p "Commit changes first? (y/n): " do_commit

        if [ "$do_commit" = "y" ]; then
            read -p "Commit message: " commit_msg
            git add -A
            git commit -m "$commit_msg"
            print_success "Changes committed"
        else
            echo "Aborting merge"
            read -p "Press Enter to continue..."
            show_menu
            return
        fi
    fi

    echo "Ready to merge $current_branch to main"
    echo ""
    read -p "Continue? (y/n): " do_merge

    if [ "$do_merge" = "y" ]; then
        # Fetch latest
        git fetch origin

        # Checkout main
        git checkout main
        print_success "Switched to main"

        # Pull latest
        git pull origin main
        print_success "Pulled latest from origin/main"

        # Merge
        git merge "$current_branch"
        print_success "Merged $current_branch into main"

        # Push
        git push origin main
        print_success "Pushed to origin/main"

        echo ""
        print_success "Deployment ready!"
        echo "Railway will automatically detect the push and redeploy."
        echo ""
        echo "Don't forget to set environment variables in Railway dashboard!"
        echo "See: RAILWAY_DEPLOYMENT_GUIDE.md"
    fi

    echo ""
    read -p "Press Enter to continue..."
    show_menu
}

show_env_template() {
    print_header "Railway Environment Variables Template"

    echo "Copy and paste these in Railway Dashboard > Variables:"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "# Required - OpenAI"
    echo "OPENAI_API_KEY=sk-proj-your-real-api-key-here"
    echo ""
    echo "# Security - Authentication"
    echo "REQUIRE_AUTH=true"
    echo "ACCESS_CODE=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))" 2>/dev/null || echo "generate-with-option-1")"
    echo ""
    echo "# Security - Rate Limiting (Production)"
    echo "MAX_TRANSCRIPTIONS_PER_HOUR=3"
    echo "MAX_SEARCHES_PER_MINUTE=10"
    echo "MAX_CHATS_PER_MINUTE=5"
    echo ""
    echo "# Optional - Models (uses defaults if not set)"
    echo "# WHISPER_MODEL=whisper-1"
    echo "# EMBEDDING_MODEL=text-embedding-ada-002"
    echo "# CHAT_MODEL=gpt-4-turbo-preview"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Note: Replace the values with your actual credentials!"
    echo ""

    read -p "Press Enter to continue..."
    show_menu
}

syntax_check() {
    print_header "Run Syntax Checks"

    if command -v python3 &> /dev/null; then
        echo "Checking Python syntax..."
        echo ""

        files=("app_gradio.py" "src/security.py" "src/transcriber.py" "src/rag_engine.py" "config.py")

        all_good=true
        for file in "${files[@]}"; do
            if [ -f "$file" ]; then
                if python3 -m py_compile "$file" 2>/dev/null; then
                    print_success "$file - OK"
                else
                    print_error "$file - SYNTAX ERROR"
                    all_good=false
                fi
            fi
        done

        echo ""
        if [ "$all_good" = true ]; then
            print_success "All files passed syntax check!"
        else
            print_error "Some files have syntax errors. Fix them before deploying."
        fi
    else
        print_error "Python3 not found"
    fi

    echo ""
    read -p "Press Enter to continue..."
    show_menu
}

# Start
show_menu
