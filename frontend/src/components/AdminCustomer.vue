<template>
    <div class="admin-customer">
      <h1>Customer Management</h1>
      <div v-if="loading">Loading...</div>
      <div v-if="error" class="error-message">{{ error }}</div>
      <div v-if="customers.length">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Phone</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="customer in customers" :key="customer.id">
              <td>{{ customer.id }}</td>
              <td>{{ customer.name }}</td>
              <td>{{ customer.email }}</td>
              <td>{{ customer.phone }}</td>
              <td>
                <button @click="updateCustomer(customer.id)" class="btn btn-secondary">Update</button>
                <button @click="deleteCustomer(customer.id)" class="btn btn-danger">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else-if="!loading && !customers.length">No customers available.</div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'AdminCustomer',
    data() {
      return {
        customers: [],
        loading: true,
        error: ''
      };
    },
    async created() {
      try {
        const response = await axios.get('http://127.0.0.1:5001/api/admin/customer/details');
        console.log('API Response:', response.data);
        this.customers = response.data.customers;
        console.log('Customers:', this.customers);
      } catch (error) {
        console.error('Error fetching customers:', error);
        this.error = 'Failed to fetch customers. Please try again later.';
      } finally {
        this.loading = false;
      }
    },
    // methods: {
    //   updateCustomer(customerId) {
    //     // Implement the logic to update the customer
    //     console.log(`Update customer with ID: ${customerId}`);
    //     // You can navigate to an update form or open a modal for updating the customer
    //   },
    //   async deleteCustomer(customerId) {
    //     try {
    //       await axios.delete(`http://127.0.0.1:5001/api/admin/customers/delete/${customerId}`);
    //       this.customers = this.customers.filter(customer => customer.id !== customerId);
    //     } catch (error) {
    //       console.error('Error deleting customer:', error);
    //       this.error = 'Failed to delete customer. Please try again later.';
    //     }
    //   }
    // }
  };
  </script>
  
  <style scoped>
  .admin-customer {
    text-align: center;
    padding: 50px;
  }
  
  h1 {
    font-size: 2.5em;
    margin-bottom: 20px;
  }
  
  .error-message {
    color: red;
    margin-top: 20px;
    font-size: 14px;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
  }
  
  th, td {
    border: 1px solid #ddd;
    padding: 12px;
    text-align: left;
  }
  
  th {
    background-color: #f4f4f4;
  }
  
  .btn {
    display: inline-block;
    padding: 10px 20px;
    margin: 5px;
    font-size: 1em;
    text-decoration: none;
    border-radius: 5px;
    transition: background-color 0.3s ease;
    cursor: pointer;
  }
  
  .btn-secondary {
    background-color: #6c757d;
    color: white;
  }
  
  .btn-secondary:hover {
    background-color: #5a6268;
  }
  
  .btn-danger {
    background-color: #dc3545;
    color: white;
  }
  
  .btn-danger:hover {
    background-color: #c82333;
  }
  </style>