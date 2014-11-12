# Raiden release notes

## V0.2-beta

### Improvements

- Non runnable images will now be ignored on run command
- Targeted containers on command line are now uniqified
- Generated internal names are now prefixes with image type
- Better dependency management
- Better docker command output, no more useless errors
- New Data image type to persistent data containers. Can't be removed without `--force` option

### Commands

- Adding possibility to target images with positional arguments
- Adding rebuild command to rebuild targeted images
- Adding clean-image command to remove containers AND their images
- `--force` option to force remove containers and images

### raiden.yml configuration file

- Adding dockerfilePrefix to set dockerfile location
- Adding `extra` option to add custom parameters to command line
- Adding `persist` option to manage volumes-from docker run options