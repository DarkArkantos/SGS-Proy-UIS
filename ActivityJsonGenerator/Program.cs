using ActivityJsonGenerator.Models;
using System;
using System.Collections.Generic;
using System.IO;
using System.Text.Json;
using System.Threading.Tasks;
using System.Linq;

namespace ActivityJsonGenerator
{
    public class Program
    {
        private const string BaseUri = @"D:\VS\Proyecto SGS UIS\SGS Proy UIS\ActivityJsonGenerator\";
        public static async Task Main(string[] args)
        {

            string[] fileArray = Directory.GetFiles($@"{BaseUri}instanciasj30\", "*.sm");
            Console.WriteLine($"Found {fileArray.Length}");
            List<Instance> instances = new List<Instance>();
            Console.WriteLine("Starting");
            var instance = await GetInstanceAsync(fileArray[0]);
            /*foreach (var item in fileArray)
            {
                instances.Add(await GetInstanceAsync(item));
            }
            using FileStream createStream = File.Create(@$"{BaseUri}\Output\instances.json");
            await JsonSerializer.SerializeAsync(createStream, instances);*/
        }

        private static async Task<Instance> GetInstanceAsync(string fileName)
        {
            string content = await File.ReadAllTextAsync(fileName);
            content = content.Substring(1);
            string[] sections = content.Split("************************************************************************");
            int index = sections[3].LastIndexOf("successors")+("successors").Length;
            string[] activities = sections[3].Substring(index).Split("\n");
            var parsedActivities = ExtractActivities(activities);
            string durations = sections[4];
            Console.WriteLine(activities);
            throw new NotImplementedException();
        }

        private static List<Activity> ExtractActivities(string[] activities)
        {
            var result = new List<Activity>();
            string[] values;
            for (int i = 1; i < activities.Length-1; i++)
            {
                values = activities[i].Split(" ")
                    .Select(item => item.Trim())
                    .Where(value => !string.IsNullOrEmpty(value))
                    .ToArray();
                var activity = new Activity
                {
                    Index = int.Parse(values[0]),
                    Precedence = new List<int>()
                };

                for (int j = 3; j < values.Length; j++)
                {
                    activity.Precedence.Add(int.Parse(values[j]));
                }

                result.Add(activity);
                Console.WriteLine(activity.Index);

            }
            return result;
        }

        private static void FixPrecedences(List<Activity> activities)
        {

        }
    }
}
