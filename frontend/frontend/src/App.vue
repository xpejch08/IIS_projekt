<template>
  <div id="app">
    <!-- User Form Example -->
    <div class="container mt-5">
      <h2>Create User</h2>
      <form @submit.prevent="createUser">
        <div class="form-group">
          <label for="name">Name:</label>
          <input
            type="text"
            class="form-control"
            v-model="userForm.name"
            required
          />
        </div>
        <div class="form-group">
          <label for="password">Password:</label>
          <input
            type="password"
            class="form-control"
            v-model="userForm.password"
            required
          />
        </div>
        <div class="form-group">
          <label for="role">Role:</label>
          <input
            type="text"
            class="form-control"
            v-model="userForm.role"
            required
          />
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
      </form>
    </div>
    <!-- Other forms and UI elements go here -->
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "App",
  data() {
    return {
      userForm: {
        name: "",
        password: "",
        role: "",
      },
      // Other data properties go here
    };
  },
  methods: {
    createUser() {
      axios
        .post("/createUser", this.userForm)
        .then((response) => {
          // Handle response
          console.log(response.data);
        })
        .catch((error) => {
          // Handle error
          console.error(error);
        });
    },
    // Other methods to delete, get, update users, add/delete subjects, create rooms go here
  },
};
</script>

<style>
/* Your CSS styles go here */
</style>
