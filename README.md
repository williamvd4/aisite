# AI Curriculum and Lesson Plan Generator

This project is a web application designed to assist educators in creating and managing curriculums and lesson plans. It leverages AI to help generate educational content, suggest activities, and streamline the planning process. Key features include user management, curriculum development tools, AI-powered lesson plan generation, and resource organization.

## Features

- **User Authentication**: Secure sign-up, login, and logout functionality.
- **Curriculum Management**: Tools for creating, viewing, editing, and organizing educational curriculums.
- **AI-Powered Lesson Plan Generation**: Smart assistance for generating lesson plans, including suggesting activities and content.
- **Resource Organization**: Upload and manage relevant educational materials and resources.
- **Interactive Calendar**: A calendar view for scheduling and tracking lessons or curriculum milestones.
- **Responsive Design**: User-friendly interface that adapts to various screen sizes.

## Manual Build

Before you begin, ensure you have Python (version 3.8 or newer) and pip installed on your system.

> 👉 **1. Clone the Repository**

```bash
$ git clone https://github.com/your-username/your-repository.git
$ cd your-repository
```
Replace `https://github.com/your-username/your-repository.git` with the actual URL of this repository.

<br />

> 👉 **2. Create and Activate a Virtual Environment**

It's recommended to use a virtual environment to manage project dependencies.

```bash
# For Windows
$ python -m venv env
$ .\env\Scripts\activate

# For macOS/Linux
$ python3 -m venv env
$ source env/bin/activate
```

<br />

> 👉 **3. Configure Environment Variables**

This project uses a `.env` file for environment variables. Copy the sample file and update it with your settings:

```bash
$ cp env.sample .env
```

Open the `.env` file and set the following critical variables:
- `SECRET_KEY`: A strong, unique secret key for your Django application. You can generate one using an online tool or Django's `get_random_secret_key()` function.
- `COHERE_API_KEY`: Your API key for Cohere, if you plan to use AI-powered features.

You may also need to configure database settings (e.g., `DB_ENGINE`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`) if you are not using the default SQLite database. For local development, SQLite is often sufficient and requires no extra configuration in `.env` beyond what's default in `settings.py`.

<br />

> 👉 **4. Install Dependencies**

Install all the required packages using pip:

```bash
$ pip install -r requirements.txt
```

<br />

> 👉 **5. Set Up Database**

Run the following commands to create the database tables:

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

<br />

> 👉 **6. Create a Superuser**

This command will prompt you to create a username and password for the Django admin interface:

```bash
$ python manage.py createsuperuser
```

<br />

> 👉 **7. Start the Development Server**

```bash
$ python manage.py runserver
```

The application should now be running at `http://127.0.0.1:8000/`.

## Codebase Structure

The project follows a standard Django layout. Key directories and files include:

```
< PROJECT ROOT >
   |
   |-- core/                            # Django project configuration
   |    |-- settings.py                  # Main project settings (database, static files, etc.)
   |    |-- urls.py                      # Project-level URL routing
   |    |-- wsgi.py                      # WSGI server configuration
   |    |-- asgi.py                      # ASGI server configuration
   |
   |-- home/                            # Main application directory
   |    |-- models.py                    # Database models for the application
   |    |-- views.py                     # Application views (request handling logic)
   |    |-- urls.py                      # App-specific URL routing
   |    |-- forms.py                     # Django forms
   |    |-- templates/                   # HTML templates for rendering pages
   |    |   |-- home/pages/              # Page-specific templates
   |    |   |-- home/includes/           # Reusable template snippets
   |    |-- ai/                          # Modules related to AI features
   |    |   |-- ai_chat.py               # AI chat functionalities
   |    |   |-- ai_review.py             # AI review functionalities
   |    |   |-- ai_utils.py              # Utility functions for AI features
   |
   |-- curriculums/                     # Storage for uploaded curriculum documents (e.g., PDFs)
   |
   |-- static/                          # Project-wide static assets
   |    |-- css/                         # CSS stylesheets
   |    |-- js/                          # JavaScript files
   |    |-- img/                         # Image files
   |    |-- react/                       # React frontend components (if applicable)
   |
   |-- staticfiles/                     # Collected static files for deployment (managed by Django)
   |
   |-- .env                             # Environment variables (create from env.sample)
   |-- env.sample                       # Sample environment variables file
   |-- Dockerfile                       # Instructions to build the Docker image
   |-- docker-compose.yml               # Docker Compose configuration
   |-- requirements.txt                 # Python package dependencies
   |-- manage.py                        # Django's command-line utility
   |-- README.md                        # This file
   |-- LICENSE.md                       # Project license
   |
   |-- ************************************************************************
```

## Usage

After successfully installing and starting the application (see "Manual Build" or "Deployment"), you can access it in your web browser.

1.  **Navigate to the Application**:
    *   If running locally, open your browser and go to `http://127.0.0.1:8000/`.
    *   If deployed, use your specific deployment URL.
    *   You will likely be greeted by the `Welcome` page.

2.  **Authentication**:
    *   On the `Welcome` page, you can `Sign Up` for a new account or `Log In` if you already have one.

3.  **Homepage/Dashboard**:
    *   After logging in, you'll be directed to the `Home` page, which serves as your main dashboard and provides access to various features.

4.  **Curriculum Management**:
    *   Navigate to the `My Curriculums` section from the dashboard or navigation menu.
    *   Here, you can create new curriculums, upload existing curriculum documents, and view or manage your existing ones.

5.  **Lesson Plan Creation**:
    *   Access the `My Lesson Plans` section.
    *   To create a new lesson, navigate to `Create New Lesson`.
    *   This form will allow you to input lesson details. The application also features AI assistance which can help generate content, suggest activities, or review your lesson plan drafts.

6.  **Resource Management**:
    *   Go to the `My Resources` section to upload, view, and organize your educational materials, such as documents, presentations, or external links.

7.  **Calendar Integration**:
    *   Visit the `My Calendar` section to view a calendar. This can be used for scheduling lessons, tracking curriculum progress, or managing important dates. You can typically add events to the calendar.

## Deployment

This project can be deployed to various platforms. Below are instructions for deploying to Render.

### Render

This project is configured for deployment on [Render](https://render.com/) using the `render.yaml` file in this repository.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

**Steps to Deploy:**

1.  **Fork this repository** to your personal GitHub account.
2.  Go to the [Render Dashboard](https://dashboard.render.com/).
3.  Click the **"New +"** button and select **"Blueprint"**.
4.  Connect your GitHub account (if you haven't already) and select your forked repository from the list.
5.  Render will automatically detect the `render.yaml` file in your repository.
6.  Assign a **Service Group Name** for your application (e.g., `ai-curriculum-generator`).
7.  **Configure Environment Variables**:
    *   Before the first deployment, navigate to the "Environment" section for your new Blueprint service.
    *   You **must** add the following environment variables:
        *   `SECRET_KEY`: A strong, unique secret key for your Django application.
        *   `COHERE_API_KEY`: Your API key for the Cohere service.
        *   `PYTHON_VERSION`: Specify the Python version used for this project (e.g., `3.11.4`). While Render might pick one, it's best to be explicit.
    *   **Database Configuration**:
        *   The provided `render.yaml` does not automatically provision a database.
        *   You will need to create a PostgreSQL database service separately on Render (Dashboard -> New + -> PostgreSQL).
        *   Once created, Render will provide a `DATABASE_URL`. Add this `DATABASE_URL` to your web service's environment variables. Your Django application's `settings.py` should be configured to parse this `DATABASE_URL` (e.g., using a library like `dj_database_url`).
8.  Click **"Create New Blueprint Instance"** (the exact wording might vary slightly on Render's interface).
9.  Render will now build and deploy your application based on the `render.yaml` and your environment variable settings. You can monitor the build and deployment progress in the logs on Render.

**Important Notes for Render Deployment:**

*   **Database**: Ensure your Django `settings.py` is configured to use the `DATABASE_URL` environment variable when available (for production on Render) and falls back to your local SQLite or other database settings for development. The `dj_database_url` Python package is commonly used for this.
*   **Static Files**: Django's `collectstatic` command should be part of your build process. The `build.sh` script (if used and referenced in `render.yaml`) typically handles this. Ensure `whitenoise` is correctly configured in your `settings.py` to serve static files in production.
*   **Allowed Hosts**: Update `ALLOWED_HOSTS` in your Django `settings.py` to include your Render service's domain (e.g., `your-app-name.onrender.com`). You can often set this via an environment variable as well.

## Contributing

Contributions are welcome and greatly appreciated! Here's how you can contribute to this project:

### Reporting Bugs

Please open an issue on the GitHub repository, providing as much detail as possible, including:
-   Steps to reproduce the bug.
-   Expected behavior.
-   Actual behavior.
-   Your environment (browser, OS, Python version, etc.).

### Suggesting Enhancements

If you have ideas for new features or improvements, please open an issue on GitHub. Describe your enhancement and its potential benefits.

### Pull Request Process

1.  **Fork the repository** on GitHub.
2.  **Clone your fork** locally: `git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git` (Replace `YOUR_USERNAME/YOUR_REPOSITORY.git` with your fork's URL).
3.  **Create a new branch**: `git checkout -b your-branch-name` (e.g., `feature/new-lesson-generator` or `fix/calendar-bug`). Use prefixes like `feature/` for new features and `fix/` for bug fixes.
4.  **Make your changes**: Implement your feature or fix the bug.
5.  **Add tests**: Write unit tests for your changes. Tests for the `home` application are located in `home/tests.py`.
6.  **Lint and Format your code**:
    *   **Python**: This project encourages adherence to PEP 8. It's recommended to use `flake8` for linting and `black` for formatting.
        ```bash
        pip install flake8 black
        flake8 .
        black .
        ```
    *   **JavaScript/TypeScript**: This project uses ESLint. The configuration can be found in `eslint.config.mjs`. Ensure your JavaScript/TypeScript code is clean and well-formatted. You may need to install ESLint globally or as a project dependency if not already set up.
        ```bash
        # If ESLint is not part of a local package.json, you might need to install it globally or set it up
        # npm install -g eslint # Example for global install
        # eslint yourfile.js # Example for running on a specific file
        ```
7.  **Test your changes**: Ensure all existing and new tests pass.
    ```bash
    python manage.py test
    ```
8.  **Commit your changes**: Use clear and descriptive commit messages.
    ```bash
    git add .
    git commit -m "feat: Add new lesson generation feature" # Or "fix: Resolve calendar display issue"
    ```
9.  **Push to your fork**: `git push origin your-branch-name`
10. **Open a Pull Request**: Go to the original project repository on GitHub and open a pull request from your branch to the `main` branch. Provide a clear description of your changes, why they were made, and reference any related issues.

### Coding Standards
-   Follow PEP 8 guidelines for Python code.
-   Write clear, concise, and well-commented code where necessary.
-   Ensure that your code is maintainable and readable.
-   For React components (if contributing to `static/react/`), follow standard React best practices.
