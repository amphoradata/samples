namespace dotnet_NEM
{
    public class EngineConfig
    {
        public string BaseUrl { get; set; } // Amphora Data host
        public string UserName { get; set; } // Amphora Data username
        public string Password { get; set; } // Amphora Data password
        public void ThrowIfInvalid()
        {
            if(string.IsNullOrEmpty(BaseUrl) || string.IsNullOrEmpty(UserName) || string.IsNullOrEmpty(Password))
            {
                throw new System.ArgumentException("Engine Config is invalid");
            }
        }
    }
}