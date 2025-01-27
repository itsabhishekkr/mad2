<template>
    <div class="login">
      <h2>Login</h2>
      <form @submit.prevent="login" class="login-form">
        <div class="form-group">
          <label for="email">Email</label>
          <input
            type="email"
            id="email"
            v-model="email"
            class="form-control"
            placeholder="Enter Email"
            required
          />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input
            type="password"
            id="password"
            v-model="password"
            class="form-control"
            placeholder="Enter Password"
            required
          />
        </div>
        <button type="submit" class="btn btn-primary" :disabled="isSubmitting">Login</button>
      </form>
  
      <!-- Display error or success messages -->
      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
      <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  export default {
    name: 'LoginPage',
    data() {
      return {
        email: '',
        password: '',
        isSubmitting: false,
        errorMessage: '',
        successMessage: ''
      };
    },
    methods: {
      async login() {
        console.log('Form submitted');
        console.log('Form data:', {
          email: this.email,
          password: this.password
        });
        this.isSubmitting = true;
        this.errorMessage = '';
        this.successMessage = '';
        try {
          const response = await axios.post('http://127.0.0.1:5001/api/login', {
            email: this.email,
            password: this.password
          });
          console.log('Response:', response);
          this.successMessage = response.data.message;
          // Store the access token in local storage
          localStorage.setItem('access_token', response.data.access_token);
          // Redirect based on role
          if (response.data.role === 'customer') {
            this.$router.push('/customer/dashboard');
          } else if (response.data.role === 'professional') {
            this.$router.push('/professional/dashboard');
          } else if (response.data.role === 'admin') {
            this.$router.push('/admin/dashboard');
          }
        } catch (error) {
          console.error('Error:', error);
          if (error.response && error.response.data) {
            this.errorMessage = error.response.data.message;
          } else {
            this.errorMessage = 'An error occurred. Please try again.';
          }
        }
        this.isSubmitting = false;
      }
    }
  };
  </script>
  
  <style scoped>
  .login {
    padding: 40px;
    max-width: 400px;
    margin: 0 auto;
    background-color: #ffffff;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    text-align: center;
  }
  
  .login h2 {
    margin-bottom: 20px;
    color: #333;
  }
  
  .form-group {
    margin-bottom: 20px;
  }
  
  .form-group label {
    font-size: 14px;
    color: #555;
    text-align: left;
    display: block;
    margin-bottom: 8px;
  }
  
  .form-group input {
    width: 100%;
    padding: 12px;
    font-size: 16px;
    border-radius: 5px;
    border: 1px solid #ddd;
    box-sizing: border-box;
    transition: border-color 0.3s ease;
  }
  
  .form-group input:focus {
    border-color: #007bff;
    outline: none;
  }
  
  .btn-primary {
    background-color: #007bff;
    color: white;
    padding: 12px 20px;
    border: none;
    border-radius: 5px;
    width: 100%;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s ease;
  }
  
  .btn-primary:hover {
    background-color: #0056b3;
  }
  
  .error-message {
    color: red;
    margin-top: 20px;
    font-size: 14px;
  }
  
  .success-message {
    color: green;
    margin-top: 20px;
    font-size: 14px;
  }
  </style>