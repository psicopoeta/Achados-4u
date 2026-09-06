// Menu Dropdown Toggle
document.addEventListener('DOMContentLoaded', function() {
    const dropdownToggle = document.querySelector('.dropdown-toggle');
    const dropdownMenu = document.querySelector('.dropdown-menu');
    
    if (dropdownToggle) {
        dropdownToggle.addEventListener('click', function(e) {
            e.preventDefault();
            dropdownMenu.style.display = dropdownMenu.style.display === 'block' ? 'none' : 'block';
        });
    }

    // Fechar menu quando clicar fora
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.dropdown')) {
            if (dropdownMenu) {
                dropdownMenu.style.display = 'none';
            }
        }
    });
});
