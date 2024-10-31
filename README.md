# Real Estate Django Project

This is a real estate web application built with Django. It allows users to search for properties, view listings, and contact agents. Agents can register on the platform, manage their listings, and communicate with clients. The application also includes a payment integration with Khalti for agent registration.

## Features

- User authentication and authorization
- Property listing management
- Search functionality
- Image upload for property listings
- Responsive design
- Agent registration with Khalti payment integration
- Inbox feature for messaging agents

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Zeusangis/django-real-estate.git
   ```
2. Navigate to the project directory:
   ```bash
   cd real-estate
   ```
3. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```
4. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
5. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
6. Set up environment variables:
   - Create a `.env` file in the project root
   - Add your Django secret key:
     ```
     SECRET_KEY=your_django_secret_key_here
     ```
   - Add your database name:
     ```
     DB_NAME=your_database_name_here
     ```
   - Add your Khalti API key:
     ```
     KHALTI_SECRET_KEY=your_khalti_secret_key_here
     ```
7. Apply migrations:
   ```bash
   python manage.py migrate
   ```
8. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
9. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Usage

- Access the application at `http://127.0.0.1:8000/`
- Log in with your superuser credentials to manage property listings
- Register as an agent using the Khalti payment integration
- Use the inbox feature to communicate with agents or clients

## Agent Registration

To register as an agent:

1. Navigate to the agent registration page
2. Fill out the required information
3. Complete the payment process using Khalti
4. Once payment is confirmed, your agent account will be activated

## Inbox Feature

The inbox feature allows users and agents to communicate within the platform:

- Send and receive messages
- View message history
- Get notifications for new messages

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries, please contact [unishk152@gmail.com](mailto:your-unishk152@gmail.com).
