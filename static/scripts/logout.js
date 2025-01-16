document.addEventListener('DOMContentLoaded', function () {
    // Logout Confirmation
    const logoutLink = document.getElementById('logout-link');
  
    if (logoutLink) {
      logoutLink.addEventListener('click', (event) => {
        event.preventDefault(); // Prevent default navigation
  
        Swal.fire({
          title: 'Are you sure?',
          text: "You won't be able to revert this!",
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#3085d6',
          cancelButtonColor: '#d33',
          confirmButtonText: 'Yes, log me out!',
          cancelButtonText: 'Cancel',
        }).then((result) => {
          if (result.isConfirmed) {
            // Redirect to logout URL if confirmed
            window.location.href = logoutLink.href;
          }
        });
      });
    }
  
    // Delete Confirmation for both POST and GET routes
    const deleteButtons = document.querySelectorAll('.delete-button');
  
    deleteButtons.forEach((button) => {
      button.addEventListener('click', function (event) {
        event.preventDefault(); // Prevent the default action
  
        const deleteUrl = this.getAttribute('data-delete-url');
        const isPostMethod = this.getAttribute('data-method') === 'POST'; // Check if method is POST
  
        Swal.fire({
          title: 'Are you sure?',
          text: "You won't be able to revert this!",
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#3085d6',
          cancelButtonColor: '#d33',
          confirmButtonText: 'Yes, delete it!',
          cancelButtonText: 'Cancel',
        }).then((result) => {
          if (result.isConfirmed) {
            if (isPostMethod) {
              // Perform a POST request if method is POST
              fetch(deleteUrl, {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                  'X-CSRFToken': '{{ csrf_token() }}',
                },
              }).then((response) => {
                if (response.ok) {
                  Swal.fire(
                    'Deleted!',
                    'The record has been deleted.',
                    'success'
                  ).then(() => {
                    location.reload(); // Reload the page after successful deletion
                  });
                } else {
                  Swal.fire(
                    'Error!',
                    'There was a problem deleting the record.',
                    'error'
                  );
                }
              });
            } else {
              // For GET request, simply redirect
              window.location.href = deleteUrl;
            }
          }
        });
      });
    });
  
    // Promote Confirmation
    const promoteButtons = document.querySelectorAll('.promote-button');
  
    promoteButtons.forEach((button) => {
      button.addEventListener('click', function (event) {
        event.preventDefault(); // Prevent default action
  
        const promoteUrl = this.getAttribute('data-promote-url');
  
        Swal.fire({
          title: 'Are you sure?',
          text: 'You are about to promote this user to Admin!',
          icon: 'info',
          showCancelButton: true,
          confirmButtonColor: '#3085d6',
          cancelButtonColor: '#d33',
          confirmButtonText: 'Yes, promote them!',
          cancelButtonText: 'Cancel',
        }).then((result) => {
          if (result.isConfirmed) {
            // Redirect to the promote URL if confirmed
            window.location.href = promoteUrl;
          }
        });
      });
    });
  
    // Demote Confirmation
    const demoteButtons = document.querySelectorAll('.demote-button');
  
    demoteButtons.forEach((button) => {
      button.addEventListener('click', function (event) {
        event.preventDefault(); // Prevent default action
  
        const demoteUrl = this.getAttribute('data-demote-url');
  
        Swal.fire({
          title: 'Are you sure?',
          text: 'You are about to demote this Admin to a Worker!',
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#ffc107',
          cancelButtonColor: '#d33',
          confirmButtonText: 'Yes, demote them!',
          cancelButtonText: 'Cancel',
        }).then((result) => {
          if (result.isConfirmed) {
            // Redirect to the demote URL if confirmed
            window.location.href = demoteUrl;
          }
        });
      });
    });
  });