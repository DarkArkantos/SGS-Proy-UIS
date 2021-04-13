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

            //string[] fileArray = Directory.GetFiles($@"{BaseUri}instanciasj30\", "*.sm");j3023_9.sm
            string[] fileArrayJ30 =
            {
                "j301_2", "j301_10", "j306_3", "j3020_7", "j3023_9", "j3044_9", "j3047_6", "j3014_3", "j3019_5", "j3037_8"
            };
            string[] fileArrayJ60 =
            {
                "j604_6" 
                //"j601_2", "j601_6", "j603_5", "j6011_8", "j6012_10", "j6014_2", "j6017_6", "j6022_10"
            };
            Console.WriteLine($"Found {fileArrayJ60.Length}");
            Console.WriteLine("Starting");
            foreach (var item in fileArrayJ60)
            {
                var instance = await GetInstanceAsync($@"{BaseUri}instanciasj60\{item}.sm");
                using FileStream createStream = File.Create(@$"{BaseUri}..\Resources\instance{item}.json");
                //, new JsonSerializerOptions { WriteIndented = true }
                await JsonSerializer.SerializeAsync(createStream, instance);
            }
        }

        private static async Task<Instance> GetInstanceAsync(string fileName)
        {
            string content = await File.ReadAllTextAsync(fileName);
            content = content.Substring(1);
            string[] sections = content.Split("************************************************************************");
            int index = sections[3].LastIndexOf("successors") + ("successors").Length;
            string[] activities = sections[3][index..].Split("\n");
            var parsedActivities = ExtractActivities(activities);
            string durations = sections[4];
            await FixPrecedences(parsedActivities);
            await SetDurations(parsedActivities, durations);
            var resources = ExtractValuesFromRow(sections[5].Split("\n")[3]);
            var instance = new Instance
            {
                Activities = parsedActivities,
                Resources = resources
            };
            return instance;
        }

        private static Task SetDurations(List<Activity> parsedActivities, string durations)
        {
            var divider = "------------------------------------------------------------------------";
            var content = durations[(durations.LastIndexOf(divider) + divider.Length)..];
            var rows = content.Split("\n");
            for (int i = 1; i < rows.Length-1; i++)
            {
                var values = ExtractValuesFromRow(rows[i]);
                parsedActivities[i-1].Duration = values[2];
                parsedActivities[i-1].Resources = values[3..];
            }
            return Task.CompletedTask;
        }

        private static List<Activity> ExtractActivities(string[] activities)
        {
            var result = new List<Activity>();
            int[] values;
            for (int i = 1; i < activities.Length - 1; i++)
            {
                values = ExtractValuesFromRow(activities[i]);
                var activity = new Activity
                {
                    Index = values[0],
                    Precedence = new List<int>()
                };

                for (int j = 3; j < values.Length; j++)
                {
                    activity.Precedence.Add(values[j]);
                }

                result.Add(activity);
                Console.WriteLine(activity.Index);

            }
            return result;
        }

        private static Task FixPrecedences(List<Activity> activities)
        {
            foreach (var activity in activities)
            {
                var res = activities
                    .Where(act => activity.Precedence.Any(p => p == act.Index))
                    .Select(act =>
                    {
                        act.Precedence.Add(activity.Index);
                        return act;
                    }).ToList();
            }
            activities.ForEach(activity => activity.Precedence.RemoveAll(p => p >= activity.Index));
            activities.OrderByDescending(act => act.Index);
            return Task.CompletedTask;
        }

        private static int[] ExtractValuesFromRow(string row)
        {
           var values = row.Split(" ")
                    .Select(item => item.Trim())
                    .Where(value => !string.IsNullOrEmpty(value))
                    .Select(value =>  int.Parse(value))
                    .ToArray();
            return values;
        }
    }
}
