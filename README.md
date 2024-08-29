# 🗨️ Chat Application

## Overview

Welcome to the **Chat Application**—a Django-based platform designed for managing chat threads and messages. This
project provides features for creating and retrieving chat threads, sending and listing messages, and tracking unread
message counts.

## Features

- **Create and Retrieve Threads:** Create new chat threads or retrieve existing ones.
- **Delete Threads:** Remove chat threads as needed.
- **List Threads:** Retrieve all threads associated with a specific user.
- **Send Messages:** Post new messages to a thread.
- **List Messages:** Retrieve messages from a specific thread or all messages.
- **Mark Messages as Read:** Update the status of messages to indicate they have been read.
- **Unread Message Count:** Get the count of unread messages for a specific user.

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Python 3.7+
- pip (Python package installer)

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/alex22201/SimpleChatIsi.git
    cd SimpleChatIsi
    ```

2. **Install the required Python packages:**

    ```bash
    pip3 install -r requirements.txt
    ```

### Configuration

3. **Configure your environment:**

   Create a `.env` file in the project root and add your environment-specific settings. You can download the example
   `.env` file and database dump from Google Drive:

   [Download .env and database dump](https://drive.google.com/drive/folders/1CHzt4sdoYM1-p3cIqzpc_qLWI70wRUTo?usp=sharing)

4. **Apply migrations:**

    ```bash
    python manage.py migrate
    ```

5. **Create a superuser (optional):**

    ```bash
    python manage.py createsuperuser
    ```

7. **Run the development server:**

    ```bash
    python manage.py runserver
    ```
