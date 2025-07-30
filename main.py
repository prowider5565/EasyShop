from flask import Flask, render_template_string
from users.handlers import user_bp
from payment.handlers import stripe_bp
from products.handlers import product_bp
from category.handlers import category_bp
from orders.handlers import orders_bp
from products.variants.handlers import variants_bp
from identity.handlers import addr_router
from flask_cors import CORS


"""
Backend dasturlashda quyidagi http metodlar bor:
    GET  - Ma'lumotlarni backenddan olib beradi.
    POST - Ma'lumotni backendga jo'natadi, ushbu ma'lumot backendni vazifasiga qarab obrabotka boladi
        Misol uchun:
            Foydalanuvchi qoshish uchun:
                {
                    "username": "Something",
                    "password": "9999"
                }
    PATCH  - Ma'lumotni ozgartiradi qisman
    PUT    - Ma'lumotni ozgartiradi qo'liq
    DELETE - Ma'lumotni ochirib tashlaydi

"""


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Store the HTML content as a raw string
HTML_CONTENT = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome Home</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow-x: hidden;
        }

        .container {
            max-width: 1200px;
            width: 100%;
            padding: 2rem;
        }

        .welcome-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            padding: 3rem;
            text-align: center;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            animation: slideUp 1s ease-out;
            position: relative;
            overflow: hidden;
        }

        .welcome-card::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            animation: shimmer 3s infinite;
            pointer-events: none;
        }

        .hero-icon {
            width: 120px;
            height: 120px;
            margin: 0 auto 2rem;
            background: linear-gradient(135deg, #ff6b6b, #feca57);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 3rem;
            animation: bounce 2s infinite;
            box-shadow: 0 10px 30px rgba(255, 107, 107, 0.3);
        }

        .title {
            font-size: 3.5rem;
            font-weight: 700;
            color: white;
            margin-bottom: 1rem;
            text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            animation: fadeInUp 1s ease-out 0.3s both;
        }

        .subtitle {
            font-size: 1.3rem;
            color: rgba(255, 255, 255, 0.9);
            margin-bottom: 2.5rem;
            line-height: 1.6;
            animation: fadeInUp 1s ease-out 0.6s both;
        }

        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin: 3rem 0;
        }

        .feature {
            background: rgba(255, 255, 255, 0.1);
            padding: 2rem;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.15);
            transition: all 0.3s ease;
            animation: fadeInUp 1s ease-out var(--delay) both;
        }

        .feature:nth-child(1) { --delay: 0.9s; }
        .feature:nth-child(2) { --delay: 1.1s; }
        .feature:nth-child(3) { --delay: 1.3s; }

        .feature:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
            background: rgba(255, 255, 255, 0.15);
        }

        .feature-icon {
            font-size: 2.5rem;
            margin-bottom: 1rem;
            display: block;
        }

        .feature h3 {
            color: white;
            font-size: 1.3rem;
            margin-bottom: 0.8rem;
            font-weight: 600;
        }

        .feature p {
            color: rgba(255, 255, 255, 0.8);
            line-height: 1.5;
        }

        .cta-button {
            display: inline-block;
            background: linear-gradient(135deg, #ff6b6b, #ee5a24);
            color: white;
            padding: 15px 40px;
            border-radius: 50px;
            text-decoration: none;
            font-weight: 600;
            font-size: 1.1rem;
            transition: all 0.3s ease;
            box-shadow: 0 10px 30px rgba(255, 107, 107, 0.4);
            animation: fadeInUp 1s ease-out 1.5s both;
            position: relative;
            overflow: hidden;
        }

        .cta-button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: left 0.5s;
        }

        .cta-button:hover::before {
            left: 100%;
        }

        .cta-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 40px rgba(255, 107, 107, 0.6);
        }

        .floating-shapes {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            overflow: hidden;
        }

        .shape {
            position: absolute;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 50%;
            animation: float 6s ease-in-out infinite;
        }

        .shape:nth-child(1) {
            width: 80px;
            height: 80px;
            top: 20%;
            left: 10%;
            animation-delay: 0s;
        }

        .shape:nth-child(2) {
            width: 60px;
            height: 60px;
            top: 60%;
            right: 10%;
            animation-delay: 2s;
        }

        .shape:nth-child(3) {
            width: 40px;
            height: 40px;
            top: 80%;
            left: 20%;
            animation-delay: 4s;
        }

        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(50px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% {
                transform: translateY(0);
            }
            40% {
                transform: translateY(-10px);
            }
            60% {
                transform: translateY(-5px);
            }
        }

        @keyframes shimmer {
            0% {
                transform: translateX(-100%) translateY(-100%) rotate(45deg);
            }
            100% {
                transform: translateX(100%) translateY(100%) rotate(45deg);
            }
        }

        @keyframes float {
            0%, 100% {
                transform: translateY(0px) rotate(0deg);
            }
            50% {
                transform: translateY(-20px) rotate(180deg);
            }
        }

        @media (max-width: 768px) {
            .container {
                padding: 1rem;
            }
            
            .welcome-card {
                padding: 2rem;
            }
            
            .title {
                font-size: 2.5rem;
            }
            
            .subtitle {
                font-size: 1.1rem;
            }
            
            .features {
                grid-template-columns: 1fr;
                gap: 1.5rem;
            }
        }
    </style>
</head>
<body>
    <div class="floating-shapes">
        <div class="shape"></div>
        <div class="shape"></div>
        <div class="shape"></div>
    </div>
    
    <div class="container">
        <div class="welcome-card">
            <div class="hero-icon">
                🏠
            </div>
            
            <h1 class="title">Welcome Home</h1>
            <p class="subtitle">Your journey to something amazing begins here. Experience the perfect blend of innovation, design, and functionality.</p>
            
            <div class="features">
                <div class="feature">
                    <span class="feature-icon">🚀</span>
                    <h3>Lightning Fast</h3>
                    <p>Built with performance in mind, delivering blazing fast experiences that keep you ahead of the curve.</p>
                </div>
                
                <div class="feature">
                    <span class="feature-icon">🎨</span>
                    <h3>Beautiful Design</h3>
                    <p>Crafted with attention to detail and modern aesthetics that provide an intuitive and delightful user experience.</p>
                </div>
                
                <div class="feature">
                    <span class="feature-icon">🔒</span>
                    <h3>Secure & Reliable</h3>
                    <p>Your data and privacy are our top priority. Built with enterprise-grade security and reliability standards.</p>
                </div>
            </div>
            
            <a href="#" class="cta-button">Get Started</a>
        </div>
    </div>
    
    <script>
        // Add some interactive sparkle effects
        document.addEventListener('mousemove', function(e) {
            const sparkle = document.createElement('div');
            sparkle.style.position = 'absolute';
            sparkle.style.left = e.clientX + 'px';
            sparkle.style.top = e.clientY + 'px';
            sparkle.style.width = '4px';
            sparkle.style.height = '4px';
            sparkle.style.background = 'white';
            sparkle.style.borderRadius = '50%';
            sparkle.style.pointerEvents = 'none';
            sparkle.style.opacity = '0.8';
            sparkle.style.animation = 'sparkle 1s ease-out forwards';
            document.body.appendChild(sparkle);
            
            setTimeout(() => {
                sparkle.remove();
            }, 1000);
        });
        
        // Add sparkle animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes sparkle {
                0% { opacity: 0.8; transform: scale(0); }
                50% { opacity: 1; transform: scale(1); }
                100% { opacity: 0; transform: scale(0); }
            }
        `;
        document.head.appendChild(style);
        
        // Smooth scroll for CTA button
        document.querySelector('.cta-button').addEventListener('click', function(e) {
            e.preventDefault();
            // Add your navigation logic here
            alert('Welcome! Ready to explore?');
        });
    </script>
</body>
</html>'''

@app.route('/')
def home():
    """Root endpoint that serves the HTML page directly"""
    return HTML_CONTENT

@app.route('/api/welcome-page')
def get_welcome_page():
    """API endpoint that returns the HTML content as a raw string"""
    return render_template_string(source=HTML_CONTENT)

@app.route('/api/welcome-page/raw')
def get_welcome_page_raw():
    """API endpoint that returns just the raw HTML string"""
    return HTML_CONTENT, 200, {'Content-Type': 'text/html'}

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Flask API is running successfully'
    })


app.register_blueprint(user_bp, url_prefix="/users")
app.register_blueprint(product_bp, url_prefix="/products")
app.register_blueprint(category_bp, url_prefix="/category")
app.register_blueprint(orders_bp, url_prefix="/orders")
app.register_blueprint(variants_bp, url_prefix="/variants")
app.register_blueprint(addr_router, url_prefix="/address")
app.register_blueprint(stripe_bp, url_prefix="/stripe")
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
