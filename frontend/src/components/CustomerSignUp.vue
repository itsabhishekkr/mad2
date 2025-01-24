<template>
  <div class="signup">
    <h2>Customer SignUp</h2>
    <form @submit.prevent="customer_signup" class="signup-form">
      <div class="form-group">
        <label for="fullname">Full Name</label>
        <input
          type="text"
          id="fullname"
          v-model="fullname"
          class="form-control"
          placeholder="Enter Full Name"
          required
        />
      </div>
      <div class="form-group">
        <label for="email">Email</label>
        <input
          type="email"
          id="email"
          v-model="email"
          class="form-control"
          placeholder="Enter Valid Email"
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
      <div class="form-group">
        <label for="address">Address</label>
        <input
          type="text"
          id="address"
          v-model="address"
          class="form-control"
          placeholder="Enter Address"
          required
        />
      </div>
      <div class="form-group">
        <label for="pincode">Pincode</label>
        <input
          type="text"
          id="pincode"
          v-model="pincode"
          class="form-control"
          placeholder="Enter Pincode"
          required
        />
      </div>
      <button type="submit" class="btn btn-primary" :disabled="isSubmitting">Sign Up</button>
    </form>

    <!-- Display error or success messages -->
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'CustomerSignUp',
  data() {
    return {
      fullname: '',
      email: '',
      password: '',
      address: '',
      pincode: '',
      isSubmitting: false,
      errorMessage: '',
      successMessage: ''
    };
  },
  methods: {
    async customer_signup() {
      console.log('Form submitted');
      console.log('Form data:', {
        fullname: this.fullname,
        email: this.email,
        password: this.password,
        address: this.address,
        pincode: this.pincode
      });
      this.isSubmitting = true;
      this.errorMessage = '';
      this.successMessage = '';
      try {
        const response = await axios.post('http://127.0.0.1:5000/api/register/customer', {
          fullname: this.fullname,
          email: this.email,
          password: this.password,
          address: this.address,
          pincode: this.pincode
        });
        console.log('Response:', response);
        this.successMessage = response.data.message;
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
.signup {
  padding: 40px;
  max-width: 400px;
  margin: 0 auto;
  background-color: #ffffff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  text-align: center;
}

.signup h2 {
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