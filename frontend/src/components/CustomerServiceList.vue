<template>
  <div>
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

    <div class="service-management">
      <div v-if="loading" class="loading">Loading...</div>
      <div v-if="error" class="error-message">{{ error }}</div>

      <div v-if="filteredServices.length" class="services-grid">
        <div v-for="service in filteredServices" :key="service.id" class="service-card" :class="{ 'booked-service': service.booked }">
          <div class="service-info">
            <h2>{{ service.name }}</h2>
            <p>{{ service.description }}</p>
            <p><strong>Price:</strong> {{ service.price }}</p>
            <p><strong>Time Required:</strong> {{ service.time_required }} hours</p>
            <button 
              @click="bookService(service.id)" 
              :class="service.booked ? 'btn btn-success' : 'btn btn-danger'"
              :disabled="service.booked"
            >
              {{ service.booked ? "Booked" : "Book Now" }}
            </button>
          </div>
        </div>
      </div>
      <div v-else-if="!loading && filteredServices.length === 0" class="no-services">No services available.</div>

      <button @click="seeBookHistory" class="btn btn-primary see-history">See Booking History</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ServiceManagement",
  data() {
    return {
      services: [],
      searchQuery: "",
      loading: true,
      error: ""
    };
  },
  computed: {
    filteredServices() {
      return this.services.filter(service =>
        service.name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    }
  },
  async created() {
    await this.fetchServices();
  },
  methods: {
    async fetchServices() {
      this.loading = true;
      this.error = "";
      try {
        const token = localStorage.getItem("access_token");
        if (!token) {
          throw new Error("Unauthorized: No token found.");
        }

        const response = await axios.get("http://127.0.0.1:5001/api/admin/service/all", {
          headers: { Authorization: `Bearer ${token}` }
        });

        this.services = response.data.services.map(service => ({
          ...service,
          booked: false
        }));
      } catch (error) {
        this.error = "Failed to fetch services. Please try again later.";
      } finally {
        this.loading = false;
      }
    },
    
    async bookService(serviceId) {
      try {
        const token = localStorage.getItem("access_token");
        if (!token) {
          this.error = "Unauthorized: No token found.";
          return;
        }

        await axios.post(`http://127.0.0.1:5001/api/customer/book/service/${serviceId}`, {}, {
          headers: { Authorization: `Bearer ${token}` }
        });

        this.services = this.services.map(service =>
          service.id === serviceId ? { ...service, booked: true } : service
        );
      } catch (error) {
        this.error = "Failed to book service. Please try again later.";
      }
    },
    seeBookHistory() {
      this.$router.push("/customer/booking/history");
    },
    logout() {
      localStorage.removeItem("access_token");
      window.location.href = "/login";
    }
  }
};
</script>

<style scoped>
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

.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  padding: 20px;
}

.service-card {
  background: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: left;
  transition: transform 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.service-card:hover {
  transform: scale(1.05);
}

.booked-service {
  background-color: #d4edda;
  border: 2px solid #28a745;
}

.service-info {
  text-align: center;
}

.see-history {
  margin-top: 20px;
  padding: 10px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}

.see-history:hover {
  background-color: #0056b3;
}
</style>

