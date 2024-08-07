# if running bash
if [ -n "$BASH_VERSION" ]; then
    # include .bashrc if it exists
    if [ -f "$HOME/.bashrc" ]; then
        . "$HOME/.bashrc"
    fi
fi

# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/bin" ] ; then
    PATH="$HOME/bin:$PATH"
fi

# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/.local/bin" ] ; then
    PATH="$HOME/.local/bin:$PATH"
fi

export ENVIRONMENT=staging
export DJANGO_SETTINGS_MODULE=settings.staging

export CACHE_MIDDLEWARE_ALIAS=
export CACHE_MIDDLEWARE_SECONDS=
export CACHE_MIDDLEWARE_KEY_PREFIX=

export DB_ENGINE=django.db.backends.mysql
export DB_NAME=toremember
export DB_USER=admin
export DB_PASSWORD=
export DB_HOST=toremember-dev.c68kupszimwv.us-east-1.rds.amazonaws.com
export DB_PORT=3306

export SECURE_SSL_REDIRECT=true

export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=
export AWS_STORAGE_BUCKET_NAME=2remember-staging

export EMAIL_BACKEND=
export SENDGRID_API_KEY=

export SENTRY_DSN=

export STRIPE_DEBUG=true
export STRIPE_DEFAULT_PLAN=
export STRIPE_PUBLIC_KEY=
export STRIPE_SECRET_KEY=
