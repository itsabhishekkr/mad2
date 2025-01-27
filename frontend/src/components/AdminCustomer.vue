<template>
  <div class="admin-customer">
    <h1>Customer Management</h1>
    <div v-if="loading" class="loading-message">Loading customer details...</div>
    <div v-if="error" class="error-message">{{ error }}</div>
    <div v-if="customers.length">
      <table>
        <thead>
          <tr>
            <th>Customer ID</th>
            <th>Full Name</th>
            <th>Email</th>
            <th>Pincode</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="customer in customers" :key="customer.customer_id">
            <td>{{ customer.customer_id }}</td>
            <td>{{ customer.fullname }}</td>
            <td>{{ customer.email }}</td>
            <td>{{ customer.pincode }}</td>
            <td>{{ customer.is_active ? 'Active' : 'Inactive' }}</td>
            <td>
              <button @click="toggleCustomerStatus(customer)" class="btn">
                {{ customer.is_active ? 'Block' : 'Unblock' }}
              </button>
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
      error: '',
      loading: true,
    };
  },
  async created() {
    try {
      const token = localStorage.getItem('access_token'); // Retrieve the token from local storage
      const response = await axios.get('http://127.0.0.1:5001/api/admin/customer/details', {
        headers: {
          Authorization: `Bearer ${token}` // Include the token in the Authorization header
        }
      });
      this.customers = response.data.customers || []; 
      console.log(this.customers);
    } catch (error) {
      this.error = `Failed to fetch customers. Please try again later. Error: ${error.message}`;
      console.error(error);
    } finally {
      this.loading = false;
    }
  },
  methods: {
    async toggleCustomerStatus(customer) {
      try {
        const token = localStorage.getItem('access_token');
        const endpoint = `http://127.0.0.1:5001/api/admin/customer/${customer.is_active ? 'block' : 'unblock'}/${customer.customer_id}`;
        await axios.put(endpoint, {}, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        customer.is_active = !customer.is_active; // Toggle the status locally
      } catch (error) {
        this.error = `Failed to ${customer.is_active ? 'block' : 'unblock'} customer. Please try again later. Error: ${error.message}`;
        console.error(error);
      }
    }
  }
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

.btn {
  padding: 5px 10px;
  margin: 5px;
  cursor: pointer;
  border: none;
  border-radius: 3px;
  background-color: #007bff;
  color: white;
}

.btn:hover {
  background-color: #0056b3;
}
</style>
