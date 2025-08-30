# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Running the Development Server
```bash
# Activate virtual environment first
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Run development server
python manage.py runserver
```

### Database Operations
```bash
# Apply migrations
python manage.py migrate

# Create new migrations after model changes
python manage.py makemigrations

# Create superuser for admin access
python manage.py createsuperuser
```

### Testing
```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test accounts
python manage.py test order
python manage.py test dashboard
python manage.py test rank
```

### Shell Access
```bash
# Access Django shell
python manage.py shell

# Access database shell
python manage.py dbshell
```

## Architecture Overview

This is a Django REST Framework backend for an automated trading system. The project follows a modular architecture with domain-specific apps.

### Core Structure

**Main Configuration (`trade_config/`)**
- `settings.py`: Django settings with Korean localization (Asia/Seoul timezone, ko-kr language)
- `urls.py`: Main URL router directing to `/api/v1/` endpoints
- `api_urls.py`: Centralized API routing for all app endpoints
- Custom user model: `accounts.User` with API key storage for trading platform integration

**Authentication & User Management (`accounts/`)**
- Custom User model extending AbstractUser with `api_key` and `secret_key` fields for trading API integration
- `UserToken` model for managing OAuth-style access/refresh tokens with expiration
- Views split into:
  - `auth.py`: Token management (get/delete access tokens)
  - `account.py`: Account information and cash deposit details
- Endpoints under `/api/v1/accounts/`

**Trading Orders (`order/`)**
- Views organized by operation type:
  - `buy_views.py`: Stock purchase operations
  - `sell_views.py`: Stock selling operations
  - `modify_views.py`: Order modification logic
- Primary endpoint: `/api/v1/order/buy/`

**Dashboard (`dashboard/`)**
- Provides trading data visualization and account summaries
- Endpoints under `/api/v1/dashboard/`

**Ranking System (`rank/`)**
- User performance ranking based on trading metrics
- Endpoints under `/api/v1/rank/`

**Utilities (`utils/`)**
- `tr_request.py`: Critical trading request handler
  - `TrRequest` class manages HTTP sessions for trading API calls
  - Handles user token injection into request headers
  - Supports both real (`KIWOOM_DOMAIN`) and mock (`MOTOO_DOMAIN`) trading environments
  - Uses connection pooling for performance
- `normalizers.py`: Data normalization utilities

### Key Technical Patterns

**Environment-Based Configuration**
- Trading environment switching via `KIWOOM_DOMAIN` (real) and `MOTOO_DOMAIN` (mock) environment variables
- Token-based authentication with Bearer tokens in HTTP headers

**Request Flow**
1. All API requests route through `/api/v1/` prefix
2. User authentication via Bearer tokens managed by `UserToken` model
3. Trading requests use `TrRequest.request_post()` with automatic token injection
4. Session reuse for efficient connection management

**Data Models**
- Custom User model with trading API credentials
- Token management with expiration tracking
- SQLite database for development (configured in settings)

### Important Considerations

- The system integrates with Kiwoom Securities REST API (키움증권)
- All timestamps use Asia/Seoul timezone
- Authentication required for most endpoints (Bearer token in Authorization header)
- Trading requests distinguish between real ('R') and mock environments
- Connection pooling is implemented at class level in `TrRequest` for performance