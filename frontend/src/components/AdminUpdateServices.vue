<template>
  <div class="admin-update-services">
    <h1>Update Service</h1>
    <div v-if="loading" class="loading-message">Loading service details...</div>
    <div v-else>
      <form @submit.prevent="updateService" class="update-form">
        <div class="form-group">
          <label for="name">Name</label>
          <input
            type="text"
            id="name"
            v-model="service.name"
            class="form-control"
            required
            placeholder="Enter service name"
          />
        </div>

        <div class="form-group">
          <label for="description">Description</label>
          <textarea
            id="description"
            v-model="service.description"
            class="form-control"
            rows="4"
            required
            placeholder="Enter service description"
          ></textarea>
        </div>

        <div class="form-group">
          <label for="price">Price</label>
          <input
            type="number"
            id="price"
            v-model="service.price"
            class="form-control"
            required
            placeholder="Enter service price"
          />
        </div>

        <div class="form-group">
          <label for="time_required">Time Required (hours)</label>
          <input
            type="number"
            id="time_required"
            v-model="service.time_required"
            class="form-control"
            required
            placeholder="Enter time required in hours"
          />
        </div>

        <button type="submit" class="btn btn-primary">Update Service</button>
      </form>
    </div>

    <div v-if="error" class="error-message">{{ error }}</div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AdminUpdateServices',
  data() {
    return {
      service: {
        id: '',
        name: '',
        description: '',
        price: '',
        time_required: ''
      },
      error: '',
      loading: true
    };
  },
  async created() {
    const serviceId = this.$route.params.id; // Get the service ID from the route
    try {
      const token = localStorage.getItem("access_token"); // Retrieve token from local storage
      console.log('Token:', token);
      const response = await axios.get(
        `http://127.0.0.1:5001/api/admin/service/one/${serviceId}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      this.service = response.data.service;
    } catch (error) {
      console.error('Error fetching service:', error);
      this.error = 'Failed to fetch service. Please try again later.';
    } finally {
      this.loading = false;
    }
  },
  methods: {
    async updateService() {
      try {
        const token = localStorage.getItem('access_token');
        await axios.put(
          `http://127.0.0.1:5001/api/admin/service/update/${this.service.id}`, // Use the actual service ID
          this.service,
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );
        this.$router.push('/admin/services');
      } catch (error) {
        console.error('Error updating service:', error);
        this.error = 'Failed to update service. Please try again later.';
      }
    }
  }
};
</script>

<style scoped>
.admin-update-services {
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

.update-form {
  max-width: 600px;
  margin: 0 auto;
  text-align: left;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border-radius: 5px;
  border: 1px solid #ddd;
}

textarea {
  resize: vertical;
}

.btn-primary {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.error-message {
  color: red;
  margin-top: 20px;
  font-size: 14px;
}
</style>

