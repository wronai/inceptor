### **1. Minimal Architecture (3 poziomy):**
- **LIMBO**: Problem → Komponenty  
- **DREAM**: Komponenty → Technical specs
- **REALITY**: Specs → Kod

### **2. Zero dependencies oprócz:**
- `requests` (do Ollama)
- `json` (built-in)

### **3. Proste użycie:**

```bash
# Command line
python inceptor.py "system logowania Flask"

# Interactive mode  
python inceptor.py

# Programmatic
from inceptor import quick_solution
result = quick_solution("CI/CD pipeline")
```

## 💻 **Przykład działania:**

```bash
🌀 Simple Dream Architect
==============================
✅ Ollama connection: OK

🎯 Describe your problem: system logowania dla Flask app

🌀 Inception starting for: system logowania dla Flask app
📊 Level 1: LIMBO - Meta Architecture...
   Components: ['authentication', 'session_management', 'user_database']
🎭 Level 2: DREAM - Solution Design...  
   Architecture: Flask app z SQLAlchemy i session management
🌍 Level 3: REALITY - Implementation...
   Files: ['app.py', 'models.py', 'config.py']

==================================================
📋 RESULTS:
==================================================

🏗️ ARCHITECTURE:
   Flask app z SQLAlchemy i session management

💻 TECHNOLOGIES:
   • Flask
   • SQLAlchemy
   • bcrypt

📁 GENERATED FILES:

--- app.py ---
from flask import Flask, request, session
from models import User, db
import bcrypt

app = Flask(__name__)
app.secret_key = 'your-secret-key'

@app.route('/login', methods=['POST'])
def login():
    # Login implementation
    ...

💾 Save files? (y/n): y
   ✅ Saved: output/app.py
   ✅ Saved: output/models.py  
   ✅ Saved: output/config.py
```

## 🔧 **Quick Functions:**

```python
# Tylko kod, bez verbose
files = just_code("monitoring system")
print(files['main.py'])

# Pełne rozwiązanie
solution = quick_solution("REST API z auth")
print(solution['dream']['architecture'])
```

## ⚡ **Setup w 30 sekund:**

```bash
# 1. Uruchom Ollama
ollama serve
ollama pull mistral:7b

# 2. Skopiuj kod do inceptor.py

# 3. Uruchom
python inceptor.py "twój problem"
```

## 🎪 **Dlaczego to działa:**

1. **Prosty flow**: 3 poziomy, jasny przepływ
2. **Error handling**: Fallback jeśli JSON nie parsuje  
3. **Flexible**: CLI + programmatic API
4. **Real output**: Generuje rzeczywiste pliki kodu
5. **No dependencies**: Tylko requests + built-ins

## 1. **Przykład**: "system logowania Flask"

```bash
python inceptor.py "system logowania Flask"
```

output:
```bash
🌀 Inception starting for: system logowania Flask
📊 Level 1: LIMBO - Meta Architecture...
   Components: ['Flask-Login', 'Flask-User95', 'Flask-Security-Extended']
🎭 Level 2: DREAM - Solution Design...
   Architecture: Microservice-based architecture with a frontend, backend, and database. The Flask framework will be used for the backend, and it will utilize Flask-Login, Flask-User95, and Flask-Security-Extended for authentication, user management, and extended security features respectively.
🌍 Level 3: REALITY - Implementation...
   Files: ['app.py', 'models.py', 'auth_blueprint.py', 'security_blueprint.py', 'database.py', 'tests.py']
Generated files:

=== app.py ===
from flask import Flask, Blueprint

   app = Flask(__name__)
   db = Blueprint('db', __name__, url_prefix='/api/v1/db')
   users = Blueprint('users', __name__, url_prefix='/api/v1/users')

   # Initialize extensions
   from your_app.extensions import setup_extensions
   setup_extensions(app)

   # Register blueprints
   app.register_blueprint(db)
   app.register_blueprint(users)

   if __name__ == '__main__':
       app.run(debug=True)

=== models.py ===
from flask_sqlalchemy import SQLAlchemy, UserMixin
   from flask_login import LoginManager, UserMixin as FlaskUserMixin

   db = SQLAlchemy()
   login_manager = LoginManager()

   class Role(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       name = db.Column(db.String(80), unique=True)
       users = db.relationship('User', backref='role', lazy=True)

   class User(FlaskUserMixin, db.Model):
       id = db.Column(db.Integer, primary_key=True)
       username = db.Column(db.String(60), unique=True)
       email = db.Column(db.String(120), unique=True)
       role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

   login_manager.init_app(app)

=== auth_blueprint.py ===
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_user95 import SQLAlchemyAdapter, UserManager, DBSession
from werkzeug.security import safe_str_cmp, generate_password_hash, check_password_hash
from models import User, db

auth = Blueprint('auth', __name__)
login_manager = LoginManager()
user_manager = UserManager(SQLAlchemyAdapter(db))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect(url_for('main.index'))

    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.index'))

        flash('Invalid username or password')

    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@login_manager.user_loader
def load_user(user_id):
    return user_manager.get(int(user_id))


This code creates an auth blueprint with routes for registration and login, as well as a logout function. It uses Flask-Login for handling authenticated users and Flask-User95 for managing users in the database. The `load_user` function is used by Flask-Login to load the user from the database when needed.

=== security_blueprint.py ===
from flask import Flask, Blueprint
from flask_security_extended import Security, login_required, UserMixin, db, roles_users, password_hash, password_verify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////path/to/db.sqlite3'
db = SQLAlchemy(app)
security = Security(app)

# Define User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128))
    is_active = db.Column(db.Boolean(), default=True)
    is_administrator = db.Column(db.Boolean(), default=False)

    def set_password(self, password):
        self.password = password_hash(password)

    def check_password(self, password):
        return password_verify(password, self.password)

# Define roles and users
roles_users(User, 'Reader', 'Editor', 'Manager', 'Administrator')

# Initialize database
db.create_all()

# Register blueprint for security endpoints
security.init_app(app)

# Protect routes with authentication
@app.route('/protected')
@login_required
def protected():
    return 'This is a protected route.'

if __name__ == '__main__':
    app.run(debug=True)

=== database.py ===
from flask import Flask, config
   from flask_sqlalchemy import SQLAlchemy

   app = Flask(__name__)
   app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
   db = SQLAlchemy(app)

=== tests.py ===
from flask import Flask, request, jsonify
   from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_raw_jwt
   from unittest import TestCase

   app = Flask(__name__)
   app.config['JWT_SECRET_KEY'] = 'secret_key'
   jwt = JWTManager(app)

   class AuthTest(TestCase):
       def test_login(self):
           response = self.client.post('/login', data={"username": "testuser", "password": "testpassword"})
           self.assertEqual(response.status_code, 200)
           access_token = get_raw_jwt(response.data)['access']
           self.assertIsNotNone(access_token)

       def test_register(self):
           response = self.client.post('/register', data={"username": "testuser", "password": "testpassword"})
           self.assertEqual(response.status_code, 201)

   class UserTest(TestCase):
       @jwt_required
       def test_get_user(self):
           with self.client as c:
               response = c.get('/user')
               self.assertEqual(response.status_code, 200)
               self.assertIn('username', response.json)

   class SecurityTest(TestCase):
       def test_forbidden(self):
           response = self.client.get('/admin')
           self.assertEqual(response.status_code, 403)

   if __name__ == '__main__':
       app.test_client()
```



## 2. **Przykład**: "system logowania Flask"

```bash
python inceptor.py "system logowania Flask"
```

output:
```bash
Problem: system logowania Flask
Components: 0
Tasks: 0
```



## 3. **Przykład**: "system logowania Flask"

```bash
python inceptor2.py "system logowania Flask"
```

output:
```bash
Problem: system logowania Flask
Components: 0
Tasks: 0
```