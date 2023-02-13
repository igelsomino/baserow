export const registerRealtimeEvents = (realtime) => {
  realtime.registerEvent('page_created', ({ store }, data) => {
    console.log(data) // TODO
  })
}
