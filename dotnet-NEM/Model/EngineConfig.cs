namespace dotnet_NEM
{
    public class EngineConfig
    {
        public string Host { get; set; }
        public string UserName { get; set; }
        public string Password { get; set; }
        public void ThrowIfInvalid()
        {
            if(string.IsNullOrEmpty(Host) || string.IsNullOrEmpty(UserName) || string.IsNullOrEmpty(Password))
            {
                throw new System.ArgumentException("Engine Config is invalid");
            }
        }
    }
}