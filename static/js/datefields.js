function getDatePicker() {
    var languageUA = {
        days: ['Неділя','Понеділок','Вівторок','Середа','Четвер','Пятниця','Субота'],
        daysShort: ['Нед','Пон','Вів','Сер','Чет','Пят','Суб'],
        daysMin: ['Нд','Пн','Вт','Ср','Чт','Пт','Сб'],
        months: ['Січень','Лютий','Березень','Квітень','Травень','Червень','Липень','Серпень','Вересень','Жовтень','Листопад','Грудень'],
        monthsShort: ['Січ','Лют','Бер','Кві','Тра','Чер','Лип','Сер','Вер','Жов','Лис','Гру'],
        today: 'Сьогодні',
        clear: 'Очистити',
        dateFormat: 'yyyy-mm-dd',
        timeFormat: 'hh:ii',
        firstDay: 1,
    };
    $('#id_valid_from').datepicker({
        language: languageUA,
        maxDate: new Date(),
    });
    $('#id_valid_to').datepicker({
        language: languageUA,
        maxDate: new Date(),
    });
}

$(document).ready( function() {
    getDatePicker();
});