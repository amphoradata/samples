using System.Net.Http;
using System.Threading.Tasks;
using Newtonsoft.Json;

namespace dotnet_NEM
{
    public class NEMClient
    {
        // Create a single, static HttpClient
        private static HttpClient httpClient = new HttpClient();
        const string url = "https://www.aemo.com.au/aemo/apps/api/report/5MIN";

        public NEMClient()
        {

        }

        public async Task<NEMResponse> Get5MinDataAsync()
        {
            var request = new NEMRequest();
            var response = await httpClient.PostAsJsonAsync(url, request);

            var responseBody = await response.Content.ReadAsStringAsync();
            return JsonConvert.DeserializeObject<NEMResponse>(responseBody);
        }

    }
}
