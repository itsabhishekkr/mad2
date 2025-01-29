<template>
  <div class="register-customer">
    <h2>Register as Customer</h2>
    <form @submit.prevent="registerCustomer" class="register-form">
      <div class="form-group">
        <label for="customerEmail">Email</label>
        <input
          type="email"
          id="customerEmail"
          v-model="customerEmail"
          class="form-control"
          placeholder="Enter Email"
          required
        />
      </div>
      <div class="form-group">
        <label for="customerPassword">Password</label>
        <input
          type="password"
          id="customerPassword"
          v-model="customerPassword"
          class="form-control"
          placeholder="Enter Password"
          required
        />
      </div>
      <div class="form-group">
        <label for="customerFullname">Full Name</label>
        <input
          type="text"
          id="customerFullname"
          v-model="customerFullname"
          class="form-control"
          placeholder="Enter Full Name"
          required
        />
      </div>
      <div class="form-group">
        <label for="customerAddress">Address</label>
        <input
          type="text"
          id="customerAddress"
          v-model="customerAddress"
          class="form-control"
          placeholder="Enter Address"
          required
        />
      </div>
      <div class="form-group">
        <label for="customerPincode">Pincode</label>
        <input
          type="text"
          id="customerPincode"
          v-model="customerPincode"
          class="form-control"
          placeholder="Enter Pincode"
          required
        />
      </div>
      <button type="submit" class="btn btn-primary" :disabled="isSubmitting">Register</button>
    </form>

    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'CustomerRegister',
  data() {
    return {
      customerEmail: '',
      customerPassword: '',
      customerFullname: '',
      customerAddress: '',
      customerPincode: '',
      isSubmitting: false,
      errorMessage: '',
      successMessage: '',
    };
  },
  methods: {
    async registerCustomer() {
      this.isSubmitting = true;
      this.errorMessage = '';
      this.successMessage = '';

      try {
        const token = localStorage.getItem('access_token');
        if (!token) {
          throw new Error('Authentication token is missing. Please log in.');
        }

        const response = await axios.post(
          'http://127.0.0.1:5001/api/register/customer',
          {
            email: this.customerEmail,
            password: this.customerPassword,
            fullname: this.customerFullname,
            address: this.customerAddress,
            pincode: this.customerPincode,
          },
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        this.successMessage = response.data.message;
      } catch (error) {
        this.errorMessage = error.response?.data?.message || error.message || 'An error occurred.';
      } finally {
        this.isSubmitting = false;
      }
    },
  },
};
</script>

<style scoped>
.register-customer {
  padding: 40px;
  max-width: 600px;
  margin: 0 auto;
  background-color: #ffffff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  text-align: center;
}

.register-customer h2 {
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