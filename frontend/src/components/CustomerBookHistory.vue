<template>
  <div class="container">
    <header class="header">
      <h1>Service Booking</h1>
      <nav>
        <ul>
          <li><a href="/login">Home</a></li>
          <li><a href="#">Summary</a></li>
          <li><input type="text" v-model="searchQuery" placeholder="Search Services" class="search-bar" /></li>
          <li><button @click="logout" class="btn btn-logout">Logout</button></li>
        </ul>
      </nav>
    </header>


    <!-- Main Content: Table for Booking History -->
    <table class="table table-striped table-hover mt-5">
      <thead class="table-header">
        <tr>
          <th>Service Name</th>
          <th>Status</th>
          <th>Date of Request</th>
          <th>Professional</th>
          <th>Email</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in bookings" :key="index">
          <td>{{ item.service_name }}</td>
          <td><span :class="statusClass(item.status)">{{ item.status }}</span></td>
          <td>{{ formatDate(item.date_of_request) }}</td>
          <td>{{ item.professional_name || 'N/A' }}</td>
          <td>{{ item.professional_email || 'N/A' }}</td>
          <td>
            <button v-if="item.status === 'accepted'" @click="closeService(index)" class="btn btn-sm btn-danger">Close</button>
            <router-link v-else-if="item.status === 'completed'" :to="`/feedback/${index}`" class="btn btn-sm btn-primary">Feedback</router-link>
            <em v-else class="awaiting">Awaiting Acceptance</em>
          </td>
        </tr>
      </tbody>
    </table>

    <router-link to="/dashboard" class="btn btn-secondary mt-3">Back to Dashboard</router-link>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'BookingHistory',
  data() {
    return {
      bookings: []
    };
  },
  async created() {
    await this.fetchBookingHistory();
  },
  methods: {
    async fetchBookingHistory() {
      try {
        const token = localStorage.getItem("access_token");
        if (!token) {
          alert("Unauthorized: Please log in.");
          this.$router.push("/login");
          return;
        }

        const response = await axios.get("http://127.0.0.1:5001/api/customer/book/history", {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.bookings = response.data.bookings;
      } catch (error) {
        console.error("Error fetching booking history:", error);
      }
    },
    async closeService(index) {
      try {
        const booking = this.bookings[index];
        await axios.post(`http://127.0.0.1:5001/api/customer/close_request/${booking.id}`);
        alert("Service closed successfully!");
        this.fetchBookingHistory();
      } catch (error) {
        console.error("Error closing service:", error);
      }
    },
    logout() {
      localStorage.removeItem("access_token");
      this.$router.push("/login");
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toISOString().split('T')[0];
    },
    statusClass(status) {
      return {
        'text-success': status === 'completed',
        'text-warning': status === 'accepted',
        'text-danger': status === 'pending'
      };
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  padding-top: 80px; /* Adjust padding to make space for the fixed navbar */
}

.header {
  text-align: center;
  margin-bottom: 20px;
}

.title {
  font-size: 2rem;
  color: #333;
  margin-bottom: 10px;
}

.navbar {
  margin-bottom: 20px;
  z-index: 999; /* Ensure the navbar stays on top */
  width: 100%; /* Ensure the navbar is full-width */
}

.navbar-nav .nav-link {
  color: #555;
  font-size: 1.1rem;
  margin-left: 15px;
}

.navbar-nav .nav-link:hover {
  color: #007bff;
}

.table {
  width: 100%;
  margin-top: 20px;
  border-collapse: collapse;
}

.table-header {
  background-color: #f8f9fa;
  text-align: left;
  font-weight: bold;
}

.table th, .table td {
  padding: 12px 15px;
  border-bottom: 1px solid #ddd;
}

.table tr:hover {
  background-color: #f1f1f1;
}

.text-success {
  color: #28a745;
}

.text-warning {
  color: #ffc107;
}

.text-danger {
  color: #dc3545;
}

.btn {
  font-size: 0.875rem;
  padding: 5px 10px;
}

.btn-sm {
  font-size: 0.75rem;
  padding: 3px 8px;
}

.awaiting {
  font-size: 0.9rem;
  color: #999;
  font-style: italic;
}

.btn-link {
  color: #007bff;
  text-decoration: none;
}

.btn-link:hover {
  color: #0056b3;
}

.mt-3 {
  margin-top: 1rem;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
  border: none;
}

.btn-secondary:hover {
  background-color: #5a6268;
}

.navbar .btn-logout {
  background: none;
  border: none;
  color: #555;
  cursor: pointer;
}

.navbar .btn-logout:hover {
  color: #dc3545;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #6e7a85;
  padding: 15px 30px;
  color: white;
}

.header h1 {
  margin: 0;
}

nav ul {
  list-style: none;
  display: flex;
  align-items: center;
  gap: 20px;
}

nav ul li {
  display: inline;
}

.search-bar {
  padding: 5px;
  border-radius: 5px;
  border: none;
}

.btn-logout {
  background-color: #dc3545;
  color: white;
  padding: 10px 15px;
  border: none;
  cursor: pointer;
}

.btn-logout:hover {
  background-color: #c82333;
}

.service-management {
  text-align: center;
  padding: 50px;
}

h1 {
  font-size: 2.5em;
  margin-bottom: 20px;
}

.loading, .error-message, .no-services {
  font-size: 18px;
  color: red;
  margin-top: 20px;
}
</style>

