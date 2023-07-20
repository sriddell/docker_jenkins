Use the following script in the script console to generate the plugins.txt file to match that of a given jenkins instance you want to simulate

```groovy
Jenkins.instance.pluginManager.plugins.each{
  plugin -> 
    println ("${plugin.getShortName()}: ${plugin.getVersion()}")
}
```

Using the same version of Jenkins and a plugins.txt from that script should exactly match the instance you want to simulate w/o plugin conflicts.