const config = {
    host: process.env.REACT_APP_API_HOST ?? '',
    user_service_url: process.env.REACT_APP_USER_SERVICE_URL ?? '',
    discussion_service_url: process.env.REACT_APP_DISCUSSION_SERVICE_URL ?? '',
}
export default config;