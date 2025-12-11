
---

## Overview

This assignment simply demonstrates the practical implementation of **Kerberos** in a client-server authentication systems. In this assignment, you'll face the implemention of a simple **Key Distribution Center (KDC)**, a **Ticket Granting Server (TGS)**, and a **Service** using Python's `requests-kerberos` package to simulate secure communication between clients and services.

---

## Objective

The goal of this assignment is to:
- Understand how **Kerberos** is used for secure, ticket-based authentication between clients and services.
- Use the `requests-kerberos` library to authenticate API requests in a Flask-based application.

---

## Kerberos Overview

**Kerberos** is a network authentication protocol that uses tickets to allow nodes to prove their identity over a non-secure network in a secure manner. It uses the concept of a trusted third party called the **Key Distribution Center (KDC)** to issue **tickets** that enable access to services without having to send passwords over the network.

Key components of Kerberos:
- **KDC (Key Distribution Center)**: Responsible for authenticating users and issuing tickets.
- **TGS (Ticket Granting Server)**: Issues service tickets based on the ticket-granting ticket (TGT) from the KDC.
- **Service**: The application or resource a user wants to access using their Kerberos ticket.

### How Kerberos Works:

1. **User Authentication**: The user authenticates against the KDC using their username and password.
2. **Ticket-Granting Ticket (TGT)**: If authenticated, the KDC provides a TGT that can be used to request access to other services.
3. **Service Ticket**: The user presents the TGT to the TGS, which issues a service ticket for the target application or service.
4. **Access the Service**: The service verifies the service ticket and grants access to the requested resource.

---

## requests-kerberos Overview

The **requests-kerberos** library integrates **Kerberos** authentication with Python’s popular **requests** library, allowing you to make HTTP requests that use Kerberos authentication. It automates the process of handling Kerberos tickets when interacting with web services.

### Key features of `requests-kerberos`:
- **Mutual Authentication**: Ensures that both the client and server authenticate each other.
- **Ticket Based Connection with Scource Verification**

---

## Project Structure

```
.
├── kerberos_service.py.py   # The Flask application that implements the KDC, TGS, and Service.
├── kerberos-request.py      # Script that demonstrates how to make Kerberos-authenticated requests.
├── requirements.txt         # python package dependencies.
```

### Main Components:

1. **KDC (Key Distribution Center)**: Manages user registration and authentication.
2. **TGS (Ticket Granting Server)**: Verifies tickets and issues service tickets.
3. **Service**: A service that verifies service tickets and grants access based on the ticket's validity.
4. **Client**: Makes requests to the Flask API, using `requests-kerberos` for authentication.

---

## Installation and Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/AUT-basics-of-security-fall-2024/HW4.git
   cd HW4
   ```

2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask server:

   ```bash
   cd kerberos_request
   python kerberos_service.py
   ```

4. In another terminal, run the `kerberos-request.py` to make requests to the API:

   ```bash
   python kerberos-request.py
   ```

---

## Usage Example

### 1. Register a user:
You can register a new user by sending a `POST` request to `/register` with the username and password in the JSON body.

### 2. Authenticate the user:
Send a `GET` request to `/authenticate` with the username and password to get a **ticket** and **session key**.

### 3. Verify the ticket:
Send the **ticket** to `/verify_ticket` to confirm its validity.

### 4. Issue a service ticket:
Use the session key and service name to get a **service ticket** from `/issue_service_ticket`.

### 5. Verify the service ticket:
Finally, send the **service ticket** to `/verify_service_ticket` to access the requested service.

---

## Key Learning Objectives

- Understand the role of **Kerberos** in network security and authentication.
- Implement a simple authentication system using **X.509 certificates**.
- Use the **requests-kerberos** library to handle secure requests and responses.


