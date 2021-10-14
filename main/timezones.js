
    function timezones() {
        const select = document.getElementById('timezone');
        for (let index = 0; index < select.length; index++) {
            const element = select[index];
            data = (`${element.value}` +','+ `${element.text}`)

            console.log(data);
            
        }
        
    }

    timezones()
