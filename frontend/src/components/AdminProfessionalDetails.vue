<template>
    <div class="admin-professional">
      <h1>Professional Management</h1>
      <div v-if="loading" class="loading-message">Loading professional details...</div>
      <div v-if="error" class="error-message">{{ error }}</div>
      <div v-if="professionals.length">
        <table>
          <thead>
            <tr>
              <th>Professional ID</th>
              <th>Full Name</th>
              <th>Email</th>
              <th>Available Services</th>
              <th>Experience</th>
              <th>Documents</th>
              <th>Address</th>
              <th>Pincode</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="professional in professionals" :key="professional.professional_id">
              <td>{{ professional.professional_id }}</td>
              <td>{{ professional.fullname }}</td>
              <td>{{ professional.email }}</td>
              <td>{{ professional.available_services }}</td>
              <td>{{ professional.experience }}</td>
              <td>{{ professional.documents }}</td>
              <td>{{ professional.address }}</td>
              <td>{{ professional.pincode }}</td>
              <td>{{ professional.is_approved ? 'Approved' : 'Not Approved' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else-if="!loading && !professionals.length">No professionals available.</div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'AdminProfessionalDetails',
    data() {
      return {
        professionals: [],
        error: '',
        loading: true,
      };
    },
    async created() {
      try {
        const token = localStorage.getItem('access_token'); // Retrieve the token from local storage
        const response = await axios.get('http://127.0.0.1:5001/api/admin/professional/details', {
          headers: {
            Authorization: `Bearer ${token}` // Include the token in the Authorization header
          }
        });
        this.professionals = response.data.professionals || []; 
        console.log(this.professionals);
      } catch (error) {
        this.error = `Failed to fetch professionals. Please try again later. Error: ${error.message}`;
        console.error(error);
      } finally {
        this.loading = false;
      }
    }
  };
  </script>
  
  <style scoped>
  .admin-professional {
    text-align: center;
    padding: 50px;
  }
  
  h1 {
    font-size: 2.5em;
    margin-bottom: 20px;
  }
  
  .loading-message {
    font-size: 1.2em;
    margin-bottom: 20px;
  }
  
  .error-message {
    color: red;
    margin-top: 20px;
    font-size: 1em;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
    border: 1px solid #ddd;
  }
  
  th,
  td {
    border: 1px solid #ddd;
    padding: 12px;
    text-align: left;
  }
  
  th {
    background-color: #f4f4f4;
  }
  
  td {
    background-color: #fff;
  }
  </style>