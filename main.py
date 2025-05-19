from flask import Flask, render_template, request, jsonify
import hashlib
import random
import string
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_password():
    # Get form data
    first_name = request.form.get('first_name', '')
    birth_year = request.form.get('birth_year', '')
    favorite_color = request.form.get('favorite_color', '')
    hometown = request.form.get('hometown', '')

    # Create a seed from personal information
    seed = first_name + birth_year + favorite_color + hometown
    random.seed(seed)

    # Define character sets
    uppercase_letters = string.ascii_uppercase  # 26 uppercase English letters
    lowercase_letters = string.ascii_lowercase  # 26 lowercase letters
    digits = string.digits  # 10 digits from 0-9
    special_chars = string.punctuation  # 32 special characters, excluding space

    # Generate password with at least one character from each set
    password = [
        random.choice(uppercase_letters),
        random.choice(lowercase_letters),
        random.choice(digits),
        random.choice(special_chars)
    ]

    # Add more characters to reach desired length (16 characters)
    all_chars = uppercase_letters + lowercase_letters + digits + special_chars
    password.extend(random.choices(all_chars, k=12))

    # Shuffle the password
    random.shuffle(password)
    password = ''.join(password)

    # Hash the password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    return jsonify({
        'password': password,
        'hashed_password': hashed_password
    })

if __name__ == '__main__':
    # Ensure the templates directory exists
    if not os.path.exists('templates'):
        os.makedirs('templates')

    # Create the HTML template
    with open('templates/index.html', 'w') as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure Password Generator</title>
    <!-- Tailwind CSS via CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Alpine.js -->
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
</head>
<body class="bg-gray-100 min-h-screen flex items-center justify-center p-4">
    <div class="bg-white rounded-lg shadow-lg p-6 w-full max-w-md" x-data="{
        formData: {
            first_name: '',
            birth_year: '',
            favorite_color: '',
            hometown: ''
        },
        password: '',
        hashedPassword: '',
        showPassword: true,
        isGenerating: false,
        copied: false,
        
        async generatePassword() {
            this.isGenerating = true;
            const formData = new FormData();
            formData.append('first_name', this.formData.first_name);
            formData.append('birth_year', this.formData.birth_year);
            formData.append('favorite_color', this.formData.favorite_color);
            formData.append('hometown', this.formData.hometown);
            
            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    body: formData
                });
                
                if (response.ok) {
                    const data = await response.json();
                    this.password = data.password;
                    this.hashedPassword = data.hashed_password;
                }
            } catch (error) {
                console.error('Error generating password:', error);
            } finally {
                this.isGenerating = false;
            }
        },
        
        copyToClipboard() {
            const textToCopy = this.showPassword ? this.password : this.hashedPassword;
            navigator.clipboard.writeText(textToCopy).then(() => {
                this.copied = true;
                setTimeout(() => this.copied = false, 2000);
            });
        },
        
        strengthClass() {
            if (!this.password) return '';
            if (this.password.length >= 12) return 'bg-green-500';
            if (this.password.length >= 8) return 'bg-yellow-500';
            return 'bg-red-500';
        }
    }">
        <h1 class="text-2xl font-bold text-center mb-6 text-indigo-700">Secure Password Generator</h1>
        
        <div class="space-y-4 mb-6">
            <div>
                <label for="first_name" class="block text-sm font-medium text-gray-700">First Name</label>
                <input type="text" id="first_name" x-model="formData.first_name" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500">
            </div>
            
            <div>
                <label for="birth_year" class="block text-sm font-medium text-gray-700">Birth Year</label>
                <input type="text" id="birth_year" x-model="formData.birth_year" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500">
            </div>
            
            <div>
                <label for="favorite_color" class="block text-sm font-medium text-gray-700">Favorite Color</label>
                <input type="text" id="favorite_color" x-model="formData.favorite_color" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500">
            </div>
            
            <div>
                <label for="hometown" class="block text-sm font-medium text-gray-700">Hometown</label>
                <input type="text" id="hometown" x-model="formData.hometown" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500">
            </div>
        </div>
        
        <button 
            @click="generatePassword" 
            class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline transition duration-150 flex items-center justify-center"
            :disabled="isGenerating || !formData.first_name || !formData.birth_year || !formData.favorite_color || !formData.hometown"
            :class="{'opacity-50 cursor-not-allowed': isGenerating || !formData.first_name || !formData.birth_year || !formData.favorite_color || !formData.hometown}"
        >
            <svg x-show="isGenerating" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Generate Password
        </button>
        
        <div x-show="password" class="mt-6 space-y-4">
            <div class="p-4 border border-gray-300 rounded-md bg-gray-50">
                <div class="flex justify-between items-center mb-2">
                    <label class="block text-sm font-medium text-gray-700">Your Generated Password</label>
                    <div class="flex items-center">
                        <label class="relative inline-flex items-center cursor-pointer">
                            <input type="checkbox" x-model="showPassword" class="sr-only peer">
                            <div class="w-9 h-5 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-indigo-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-indigo-600"></div>
                            <span class="ml-2 text-sm font-medium text-gray-700" x-text="showPassword ? 'Plain Text' : 'Hashed'"></span>
                        </label>
                    </div>
                </div>
                
                <div class="flex items-center">
                    <input type="text" readonly x-bind:value="showPassword ? password : hashedPassword" class="block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500">
                    <button @click="copyToClipboard" class="ml-2 p-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500" :class="{'bg-green-600 hover:bg-green-700': copied}">
                        <svg x-show="!copied" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" />
                        </svg>
                        <svg x-show="copied" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                        </svg>
                    </button>
                </div>
                
                <div x-show="showPassword" class="mt-2">
                    <div class="text-sm font-medium text-gray-700 mb-1">Password Strength</div>
                    <div class="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                        <div class="h-full transition-all duration-300" :class="strengthClass()" :style="'width: ' + (password.length * 6.25) + '%'"></div>
                    </div>
                    <div class="flex justify-between text-xs text-gray-500 mt-1">
                        <span>Weak</span>
                        <span>Strong</span>
                    </div>
                </div>
            </div>
            
            <div class="bg-blue-50 border-l-4 border-blue-400 p-4 rounded">
                <div class="flex">
                    <div class="flex-shrink-0">
                        <svg class="h-5 w-5 text-blue-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2h-1V9z" clip-rule="evenodd" />
                        </svg>
                    </div>
                    <div class="ml-3">
                        <p class="text-sm text-blue-700">
                            This password is generated from your personal information but is made complex with uppercase, lowercase, digits, and special characters.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>""")

    app.run(debug=True)