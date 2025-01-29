<template>
  <div class="service-management">
    <h1>Service Management</h1>
    <div v-if="loading">Loading...</div>
    <div v-if="error" class="error-message">{{ error }}</div>
    <div v-if="services.length">
      <table>
        <thead>
          <tr>
            <th>Serial No</th>
            <th>Name</th>
            <th>Description</th>
            <th>Price</th>
            <th>Time Required</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(service,index) in services" :key="service.id">
            <td>{{index+1}}</td> 
            <td>{{ service.name }}</td>
            <td>{{ service.description }}</td>
            <td>{{ service.price }}</td>
            <td>{{ service.time_required }} hours</td>
            <td>
              <!-- Corrected router-link usage -->
              <router-link :to="{ name: 'AdminUpdateService', params: { id : service.id } }" class="btn btn-secondary">
                Update
              </router-link>
              <button @click="deleteService(service.id)" class="btn btn-danger">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else-if="!loading && !services.length">No services available.</div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ServiceManagement",
  data() {
    return {
      services: [], // Stores the services fetched from the API
      loading: true, // Indicates whether data is being loaded
      error: "" // Stores any error messages
    };
  },
  async created() {
    try {
      const token = localStorage.getItem("access_token"); // Replace with your method of storing the token
      console.log("Token:", token);
      if (!token) {
        throw new Error("Unauthorized: No token found.");
      }

      const response = await axios.get("http://127.0.0.1:5001/api/admin/service/all", {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      this.services = response.data.services || [];
    } catch (error) {
      if (error.response && error.response.status === 401) {
        console.error("Unauthorized access. Please check your credentials.");
        this.error = "Unauthorized access. Please log in.";
      } else {
        console.error("Error fetching services:", error);
        this.error = "Failed to fetch services. Please try again later.";
      }
    } finally {
      this.loading = false;
    }
  },
  methods: {
    async deleteService(serviceId) {
      try {
        const token = localStorage.getItem("access_token");
        await axios.delete(`http://127.0.0.1:5001/api/admin/service/delete/${serviceId}`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.services = this.services.filter(service => service.id !== serviceId);
      } catch (error) {
        console.error("Error deleting service:", error);
        this.error = "Failed to delete service. Please try again later.";
      }
    }
  }
};
</script>

<style scoped>
.service-management {
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

th,
td {
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
