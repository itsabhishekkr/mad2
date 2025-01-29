<template>
    <div class="register-professional">
      <h2>Professional Signup</h2>
      <form @submit.prevent="registerProfessional" enctype="multipart/form-data">
        <div class="mb-3">
          <label for="email" class="form-label">Email:</label>
          <input type="email" v-model="email" class="form-control" id="email" required />
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password:</label>
          <input type="password" v-model="password" class="form-control" id="password" required />
        </div>
        <div class="mb-3">
          <label for="fullname" class="form-label">Fullname:</label>
          <input type="text" v-model="fullname" class="form-control" id="fullname" required />
        </div>
        <div class="mb-3">
          <label for="address" class="form-label">Address:</label>
          <input type="text" v-model="address" class="form-control" id="address" required />
        </div>
        <div class="mb-3">
          <label for="available_services">Services Name:</label>
          <select v-model="available_services" class="form-control" id="available_services" required>
            <option value="" disabled selected>Select a service</option>
            <option v-for="service in services" :key="service.name" :value="service.name">
              {{ service.name }}
            </option>
          </select>
        </div>
        <div class="mb-3">
          <label for="experience" class="form-label">Experience (years):</label>
          <input type="number" v-model="experience" class="form-control" id="experience" required />
        </div>
        <div class="mb-3">
          <label for="documents" class="form-label">Upload Documents:</label>
          <input type="file" @change="handleFileUpload" class="form-control" id="documents" required />
        </div>
        <div class="mb-3">
          <label for="pincode" class="form-label">Pin Code:</label>
          <input type="text" v-model="pincode" class="form-control" id="pincode" pattern="\d{6}" minlength="6" maxlength="6" required />
          <div class="form-text">Enter a 6-digit pin code.</div>
        </div>
        <button type="submit" class="btn btn-primary" :disabled="isSubmitting">Register</button>
        <br />
        <div class="mt-3">
          <p>Already have an account?</p>
          <router-link to="/login" class="btn btn-secondary w-100">Login</router-link>
        </div>
      </form>
      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
      <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    name: "ProfessionalRegister",
    data() {
      return {
        email: "",
        password: "",
        fullname: "",
        address: "",
        available_services: "",
        experience: "",
        documents: null,
        pincode: "",
        services: [], // This will store the filtered services
        isSubmitting: false,
        errorMessage: "",
        successMessage: "",
      };
    },
    created() {
      // Fetch the available services from the backend
      this.fetchServices();
    },
    methods: {
      async fetchServices() {
        const token = localStorage.getItem("access_token");
        if (!token) {
          this.errorMessage = "Authentication token is missing. Please log in.";
          return;
        }
  
        try {
          const response = await axios.get("http://127.0.0.1:5001/api/admin/service/all", {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          console.log("API Response:", response.data);
          this.services = response.data.services
            .filter((service) => service.is_approved)
            .map((service) => ({ name: service.name }));
        } catch (error) {
          console.error("Error fetching services:", error);
          this.errorMessage = "Error fetching services. Please try again later.";
        }
      },
      handleFileUpload(event) {
        this.documents = event.target.files[0];
      },
      async registerProfessional() {
        this.isSubmitting = true;
        this.errorMessage = "";
        this.successMessage = "";
  
        try {
          const token = localStorage.getItem("access_token");
          if (!token) {
            throw new Error("Authentication token is missing. Please log in.");
          }
  
          const formData = new FormData();
          formData.append("email", this.email);
          formData.append("password", this.password);
          formData.append("fullname", this.fullname);
          formData.append("address", this.address);
          formData.append("available_services", this.available_services);
          formData.append("experience", this.experience);
          formData.append("documents", this.documents);
          formData.append("pincode", this.pincode);
  
          const response = await axios.post(
            "http://127.0.0.1:5001/api/register/professional",
            formData,
            {
              headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "multipart/form-data",
              },
            }
          );
  
          this.successMessage = response.data.message;
          // Redirect to login page after successful registration
          this.$router.push("/login");
        } catch (error) {
          this.errorMessage = error.response?.data?.message || error.message || "An error occurred.";
        } finally {
          this.isSubmitting = false;
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .register-professional {
    padding: 20px;
    max-width: 600px;
    margin: auto;
    background-color: #f9f9f9;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    font-family: 'Arial', sans-serif;
  }
  
  h2 {
    margin-bottom: 15px;
    font-size: 20px;
    color: #333;
    font-weight: 600;
    text-align: center;
  }
  
  .mb-3 {
    margin-bottom: 15px;
  }
  
  label {
    font-size: 14px;
    font-weight: 500;
    color: #555;
    display: block;
    margin-bottom: 6px;
  }
  
  input,
  select {
    width: 100%;
    padding: 10px;
    font-size: 14px;
    border-radius: 6px;
    border: 1px solid #ddd;
    box-sizing: border-box;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
    background-color: #fff;
  }
  
  input:focus,
  select:focus {
    border-color: #007bff;
    box-shadow: 0 0 4px rgba(0, 123, 255, 0.4);
    outline: none;
  }
  
  .form-text {
    font-size: 12px;
    color: #666;
    margin-top: 4px;
  }
  
  button {
    background-color: #007bff;
    color: white;
    padding: 10px 16px;
    border: none;
    border-radius: 6px;
    font-size: 14px;
    cursor: pointer;
    width: 100%;
    transition: all 0.3s ease;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  
  button:disabled {
    background-color: #a6c8ff;
    cursor: not-allowed;
  }
  
  .mt-3 {
    margin-top: 15px;
    text-align: center;
  }
  
  .mt-3 p {
    margin: 0;
    font-size: 12px;
    color: #555;
  }
  
  .mt-3 .btn-secondary {
    margin-top: 8px;
    background-color: #6c757d;
    color: white;
    padding: 10px;
    border-radius: 6px;
    text-decoration: none;
    display: inline-block;
    width: 100%;
    text-align: center;
    font-size: 14px;
    transition: background-color 0.3s ease;
  }
  
  .mt-3 .btn-secondary:hover {
    background-color: #5a6268;
  }
  
  .error-message {
    color: #d9534f;
    background-color: #f9d6d5;
    border: 1px solid #f5c6cb;
    padding: 10px;
    border-radius: 6px;
    margin-top: 15px;
    font-size: 12px;
  }
  
  .success-message {
    color: #28a745;
    background-color: #d4edda;
    border: 1px solid #c3e6cb;
    padding: 10px;
    border-radius: 6px;
    margin-top: 15px;
    font-size: 12px;
  }
  
  @media (max-width: 768px) {
    .register-professional {
      padding: 15px;
    }
  
    h2 {
      font-size: 18px;
    }
  
    button {
      font-size: 12px;
      padding: 8px;
    }
  }
  </style>
  
