document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    const nameInput = document.getElementById('name');
    const sleepTimeInput = document.getElementById('sleep_time');
    const wakeUpTimeInput = document.getElementById('wake_up_time');

    form.addEventListener('submit', submitForm);


    function submitForm(event) {
        event.preventDefault();
        const name = nameInput.value;
        const sleepTime = sleepTimeInput.value;
        const wakeUpTime = wakeUpTimeInput.value;

        console.log(`Name: ${name}`);
        console.log(`Sleep Time: ${sleepTime}`);
        console.log(`Wake Up Time: ${wakeUpTime}`);

        // Send the data to the server using AJAX or Fetch API
    }
});