export const formatDate = (dateStr) => {
    const date = new Date(dateStr)

    return date.toLocaleDateString('uk-UA', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    })
}