$(document).ready(() => {

    $('#result_list tbody tr').click((e) => {

        if (e.target.className.search("action-select") > -1 || e.target.className.search("action-checkbox") > -1)
            return

        window.location.href = $('a', e.currentTarget.children[1]).attr('href')

    })
})
