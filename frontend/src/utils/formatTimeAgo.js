export const formatTimeAgo = (dateStr) => {
    const date = new Date(dateStr + "Z");
    const diff = Date.now() - date.getTime()
    const rtf = new Intl.RelativeTimeFormat('en-US', { numeric: 'auto' })

    const seconds = Math.floor(diff / 1000)
    if (seconds < 60) return rtf.format(-seconds, 'second')

    const minutes = Math.floor(seconds / 60)
    if (minutes < 60) return rtf.format(-minutes, 'minute')

    const hours = Math.floor(minutes / 60)
    if (hours < 24) return rtf.format(-hours, 'hour')

    const days = Math.floor(hours / 24)
    if (days < 30) return rtf.format(-days, 'day')

    const months = Math.floor(days / 30)
    if (months < 12) return rtf.format(-months, 'month')

    const years = Math.floor(months / 12)
    return rtf.format(-years, 'year')
}