#!/usr/bin/env python

################################################################################
#
#  qooxdoo - the new era of web development
#
#  http://qooxdoo.org
#
#  Copyright:
#    2006-2010 1&1 Internet AG, Germany, http://www.1und1.de
#
#  License:
#    LGPL: http://www.gnu.org/licenses/lgpl.html
#    EPL: http://www.eclipse.org/org/documents/epl-v10.php
#    See the LICENSE file in the project's top-level directory for details.
#
#  Authors:
#    * Thomas Herchenroeder (thron7)
#
################################################################################

import os, sys, string, types, re, zlib, time
import urllib, urlparse, optparse, pprint
import simplejson
from generator.action.ImageInfo import ImageInfo, ImgInfoFmt
from generator.config.Lang      import Lang
from generator.config.Library   import Library
from generator.code.Part        import Part
from generator.code.Package     import Package
from ecmascript                 import compiler
from misc                       import filetool, json, Path
from misc.ExtMap                import ExtMap
from misc.Path                  import OsPath, Uri
from misc                       import securehash as sha
        

console = None

class CodeGenerator(object):

    def __init__(self, cache_, console_, config, job, settings, locale, resourceHandler, classes):
        global console, cache
        self._cache   = cache_
        self._console = console_
        self._config  = config
        self._job     = job
        self._settings     = settings
        self._locale     = locale
        self._resourceHandler = resourceHandler
        self._classes = classes

        console = console_
        cache   = cache_



    def runCompiled(self, script, treeCompiler, version="build"):

        def getOutputFile(compileType):
            filePath = compConf.get("paths/file")
            if not filePath:
                filePath = os.path.join(compileType, "script", self.getAppName() + ".js")
            return filePath

        def getFileUri(scriptUri):
            appfile = os.path.basename(fileRelPath)
            fileUri = os.path.join(scriptUri, appfile)  # make complete with file name
            fileUri = Path.posifyPath(fileUri)
            return fileUri

        def generateBootScript(globalCodes, script, bootPackage="", compileType="build"):

            def packagesOfFiles(fileUri, packages):
                # returns list of lists, each containing destination file name of the corresp. part
                # npackages = [['script/gui-0.js'], ['script/gui-1.js'],...]
                npackages = []
                file = os.path.basename(fileUri)
                if self._job.get("packages/loader-with-boot", True):
                    totalLen = len(packages)
                else:
                    totalLen = len(packages) + 1
                for packageId, packageFileName in enumerate(self.packagesFileNames(file, totalLen, classPackagesOnly=True)):
                    npackages.append((packageFileName,))
                    packages[packageId].file = packageFileName  # TODO: very unnice to fix this here
                return npackages

            # besser: fixPackagesFiles()
            def packagesOfFilesX(fileUri, packages):
                # returns list of lists, each containing destination file name of the corresp. package
                # npackages = [['script/gui-0.js'], ['script/gui-1.js'],...]
                file = os.path.basename(fileUri)
                loader_with_boot = self._job.get("packages/loader-with-boot", True)
                for packageId, package in enumerate(packages):
                    if loader_with_boot:
                        suffix = packageId - 1
                        if suffix < 0:
                            suffix = ""
                    else:
                        suffix = packageId
                    packageFileName = self._resolveFileName(file, self._variants, self._settings, suffix)
                    package.file = packageFileName

                return packages

            # ----------------------------------------------------------------------------
            self._console.info("Generating boot script...")

            if not self._job.get("packages/i18n-with-boot", True):
                globalCodes = self.writeI18NFiles(globalCodes, script)
                # remove I18N info from globalCodes, so they don't go into the loader
                globalCodes["Translations"] = {}
                globalCodes["Locales"]      = {}
            else:
                if compileType == "build":
                    # also remove them here, as this info is now with the packages
                    globalCodes["Translations"] = {}
                    globalCodes["Locales"]      = {}

            plugCodeFile = compConf.get("code/decode-uris-plug", False)
            if compileType == "build":
                filepackages = packagesOfFiles(fileUri, packages)
                bootContent = self.generateBootCode(parts, filepackages, boot, script, compConf, variants, settings, bootPackage, globalCodes, compileType, plugCodeFile, format)
            else:
                filepackages = [x.classes for x in packages]
                bootContent = self.generateBootCode(parts, filepackages, boot, script, compConf, variants={}, settings={}, bootCode=None, globalCodes=globalCodes, version=compileType, decodeUrisFile=plugCodeFile, format=format)


            return bootContent


        def getPackageData(package):
            data = {}
            data["resources"]    = package.data.resources
            data["translations"] = package.data.translations
            data["locales"]      = package.data.locales
            data = json.dumpsCode(data)
            data += ';\n'
            return data

        def compilePackage(packageIndex, package):
            self._console.info("Compiling package #%s:" % packageIndex, False)
            self._console.indent()

            # Compile file content
            pkgCode = self._treeCompiler.compileClasses(package.classes, variants, optimize, format)
            pkgData = getPackageData(package)
            hash    = sha.getHash(pkgData + pkgCode)[:12]  # first 12 chars should be enough

            isBootPackage = packageIndex == 0
            if isBootPackage:
                compiledContent = ("qx.$$packageData['%s']=" % hash) + pkgData + pkgCode
            else:
                compiledContent  = u'''qx.$$packageData['%s']=%s\n''' % (hash, pkgData)
                compiledContent += u'''qx.Part.$$notifyLoad("%s", function() {\n%s\n});''' % (hash, pkgCode)
            
            #
            package.hash = hash  # to fill qx.$$loader.packageHashes in generateBootScript()

            self._console.debug("Done: %s" % self._computeContentSize(compiledContent))
            self._console.outdent()

            return compiledContent

        # -- Main --------------------------------------------------------------

        # Early return
        compileType = self._job.get("compile/type", "")
        if compileType not in ("build", "source"):
            return

        packages   = script.packagesSortedSimple()
        parts      = script.parts
        boot       = script.boot
        variants   = script.variants

        self._classList    = script.classes
        self._treeCompiler = treeCompiler
        self._variants     = variants

        self._console.info("Generate %s version..." % compileType)
        self._console.indent()

        # - Evaluate job config ---------------------
        # Compile config
        compConf = self._job.get("compile-options")
        compConf = ExtMap(compConf)

        # Whether the code should be formatted
        format = compConf.get("code/format", False)
        script.scriptCompress = compConf.get("paths/gzip", False)

        # Read in settings
        settings = self.getSettings()
        script.settings = settings

        # Read libraries
        libs = self._job.get("library", [])

        # Get translation maps
        locales = compConf.get("code/locales", [])
        translationMaps = self.getTranslationMaps(packages, variants, locales)

        # Read in base file name
        fileRelPath = getOutputFile(compileType)
        filePath    = self._config.absPath(fileRelPath)
        script.baseScriptPath = filePath

        if compileType == "build":
            # read in uri prefixes
            scriptUri = compConf.get('uris/script', 'script')
            scriptUri = Path.posifyPath(scriptUri)
            fileUri   = getFileUri(scriptUri)
            # for resource list
            resourceUri = compConf.get('uris/resource', 'resource')
            resourceUri = Path.posifyPath(resourceUri)
        else:
            # source version needs place where the app HTML ("index.html") lives
            self.approot = self._config.absPath(compConf.get("paths/app-root", ""))
            resourceUri = None
            scriptUri   = None

        # Get global script data (like qxlibraries, qxresources,...)
        globalCodes = self.generateGlobalCodes(script, libs, translationMaps, settings, variants, format, resourceUri, scriptUri)

        if compileType == "build":

            # - Specific job config ---------------------
            # read in compiler options
            optimize = compConf.get("code/optimize", [])
            self._treeCompiler.setOptimize(optimize)

            # - Generating packages ---------------------
            self._console.info("Generating packages...")
            self._console.indent()

            bootPackage = ""
            for packageIndex, package in enumerate(packages):
                package.compiled = compilePackage(packageIndex, package)

            self._console.outdent()
            if not len(packages):
                raise RuntimeError("No valid boot package generated.")

            # - Put loader and packages together -------
            loader_with_boot = self._job.get("packages/loader-with-boot", True)
            # handle loader and boot package
            if loader_with_boot:
                bootCode = generateBootScript(globalCodes, script, packages[0].compiled)
                packages[0].compiled = bootCode
            else:
                loaderCode = generateBootScript(globalCodes, script)
                loadPackage = Package(0)            # make a dummy Package for the loader
                loadPackage.compiled = loaderCode
                packages.insert(0, loadPackage)

            # attach file names
            for package, fileName in zip(packages, self.packagesFileNames(script.baseScriptPath, len(packages))):
                package.file = fileName

            # write packages
            self.writePackages(packages, script)

        # ---- 'source' version ------------------------------------------------
        else:

            sourceContent = generateBootScript(globalCodes, script, bootPackage="", compileType=compileType)

            # Construct file name
            resolvedFilePath = self._resolveFileName(filePath, variants, settings)

            # Save result file
            filetool.save(resolvedFilePath, sourceContent)

            if compConf.get("paths/gzip"):
                filetool.gzip(resolvedFilePath, sourceContent)

            self._console.outdent()
            self._console.debug("Done: %s" % self._computeContentSize(sourceContent))
            self._console.outdent()

        self._console.outdent()

        return  # runCompiled()


    def runPrettyPrinting(self, classes, classesObj):
        "Gather all relevant config settings and pass them to the compiler"

        if not isinstance(self._job.get("pretty-print", False), types.DictType):
            return

        self._console.info("Pretty-printing code...")
        self._console.indent()
        ppsettings = ExtMap(self._job.get("pretty-print"))  # get the pretty-print config settings

        # init options
        parser  = optparse.OptionParser()
        compiler.addCommandLineOptions(parser)
        (options, args) = parser.parse_args([])

        # modify according to config
        setattr(options, 'prettyPrint', True)  # turn on pretty-printing
        if ppsettings.get('general/indent-string',False):
            setattr(options, 'prettypIndentString', ppsettings.get('general/indent-string'))
        if ppsettings.get('comments/trailing/keep-column',False):
            setattr(options, 'prettypCommentsTrailingKeepColumn', ppsettings.get('comments/trailing/keep-column'))
        if ppsettings.get('comments/trailing/comment-cols',False):
            setattr(options, 'prettypCommentsTrailingCommentCols', ppsettings.get('comments/trailing/comment-cols'))
        if ppsettings.get('comments/trailing/padding',False):
            setattr(options, 'prettypCommentsInlinePadding', ppsettings.get('comments/trailing/padding'))
        if ppsettings.get('blocks/align-with-curlies',False):
            setattr(options, 'prettypAlignBlockWithCurlies', ppsettings.get('blocks/align-with-curlies'))
        if ppsettings.get('blocks/open-curly/newline-before',False):
            setattr(options, 'prettypOpenCurlyNewlineBefore', ppsettings.get('blocks/open-curly/newline-before'))
        if ppsettings.get('blocks/open-curly/indent-before',False):
            setattr(options, 'prettypOpenCurlyIndentBefore', ppsettings.get('blocks/open-curly/indent-before'))

        self._console.info("Pretty-printing files: ", False)
        numClasses = len(classes)
        for pos, classId in enumerate(classes):
            self._console.progress(pos, numClasses)
            #tree = treeLoader.getTree(classId)
            tree = classesObj[classId].tree()
            compiled = compiler.compile(tree, options)
            filetool.save(self._classes[classId]['path'], compiled)

        self._console.outdent()

        return


    def getSettings(self):
        # TODO: Runtime settings support is currently missing
        settings = {}
        settingsConfig = self._job.get("settings", {})
        settingsRuntime = self._settings

        for key in settingsConfig:
            settings[key] = settingsConfig[key]

        for key in settingsRuntime:
            settings[key] = settingsRuntime[key]

        return settings


    def _resolveFileName(self, fileName, variants=None, settings=None, packageId=""):
        if variants:
            for key in variants:
                pattern = "{%s}" % key
                fileName = fileName.replace(pattern, str(variants[key]))

        if settings:
            for key in settings:
                pattern = "{%s}" % key
                fileName = fileName.replace(pattern, str(settings[key]))

        if packageId != "":
            fileName = fileName.replace(".js", "-%s.js" % packageId)

        return fileName


    def _computeContentSize(self, content):
        # Convert to utf-8 first
        content = unicode(content).encode("utf-8")

        # Calculate sizes
        origSize = len(content)
        compressedSize = len(zlib.compress(content, 9))

        return "%sKB / %sKB" % (origSize/1024, compressedSize/1024)


    def _computeResourceUri(self, lib, resourcePath, rType="class", appRoot=None):
        '''computes a complete resource URI for the given resource type rType, 
           from the information given in lib and, if lib doesn't provide a
           general uri prefix for it, use appRoot and lib path to construct
           one'''

        if 'uri' in lib:
            libBaseUri = Uri(lib['uri'])
        elif appRoot:
            libBaseUri = Uri(Path.rel_from_to(self._config.absPath(appRoot), lib['path']))
        else:
            raise RuntimeError, "Need either lib['uri'] or appRoot, to calculate final URI"
        #libBaseUri = Uri(libBaseUri.toUri())

        if rType in lib:
            libInternalPath = OsPath(lib[rType])
        else:
            raise RuntimeError, "No such resource type: \"%s\"" % rType

        # process the second part of the target uri
        uri = libInternalPath.join(resourcePath)
        uri = Uri(uri.toUri())

        libBaseUri.ensureTrailingSlash()
        uri = libBaseUri.join(uri)

        return uri


    def _makeVariantsName(self, pathName, variants):
        (newname, ext) = os.path.splitext(pathName)
        for key in variants:
            newname += "_%s:%s" % (str(key), str(variants[key]))
        newname += ext
        return newname


    def generateGlobalCodes(self, script, libs, translationMaps, settings, variants, format=False, resourceUri=None, scriptUri=None):
        # generate the global codes like qxlibraries, qxresources, ...
        # and collect them in a common structure

        def mergeTranslationMaps(transMaps):
            # translationMaps is a pair (po-data, cldr-data) per package:
            # translationMaps = [({'C':{},..},{'C':{},..}), (.,.), ..]
            # this function merges all [0] elements into a common dict, and
            # all [1] elements:
            # return = ({'C':{},..}, {'C':{},..})
            poData = {}
            cldrData = {}

            for pac_dat, loc_dat in transMaps:
                for loc in pac_dat:
                    if loc not in poData:
                        poData[loc] = {}
                    poData[loc].update(pac_dat[loc])
                for loc in loc_dat:
                    if loc not in cldrData:
                        cldrData[loc] = {}
                    cldrData[loc].update(loc_dat[loc])

            return (poData, cldrData)


        globalCodes  = {}

        globalCodes["Settings"]    = settings

        variantInfo = self.generateVariantsCode(variants)
        globalCodes["Variants"]    = variantInfo

        mapInfo = self.generateLibInfoCode(libs, format, resourceUri, scriptUri)
        # add synthetic output lib
        if scriptUri:
            out_sourceUri = scriptUri
        else:
            out_sourceUri = self._computeResourceUri({'class': ".", 'path': os.path.dirname(script.baseScriptPath)}, OsPath(""), rType="class", appRoot=self.approot)
            out_sourceUri = os.path.normpath(out_sourceUri.encodedValue())
        mapInfo['__out__'] = { 'sourceUri': out_sourceUri }
        globalCodes["Libinfo"]     = mapInfo

        #import cProfile
        #cProfile.runctx("mapInfo = self.generateResourceInfoCode(script, settings, libs, format)", globals(), locals(), "/home/thron7/tmp/generateResourceIC.profile")
        mapInfo = self.generateResourceInfoCode(script, settings, libs, format)
        globalCodes["Resources"]    = mapInfo

        locData = mergeTranslationMaps(translationMaps)
        globalCodes["Translations"] = locData[0] # 0: .po data
        globalCodes["Locales"]      = locData[1] # 1: cldr data

        return globalCodes


    def generateVariantsCode(self, variants):
        variats = {}

        for key in variants:
            if key in Lang.META_KEYS:
                continue
            variats[key] = variants[key]

        return variats


    def getTranslationMaps(self, packages, variants, locales):
        if "C" not in locales:
            locales.append("C")

        self._console.info("Processing translations for %s locales..." % len(locales))
        self._console.indent()

        packageTranslations = []
        i18n_with_packages  = self._job.get("packages/i18n-with-boot", True)
        for pos, package in enumerate(packages):
            self._console.debug("Package: %s" % pos)
            self._console.indent()

            pac_dat = self._locale.getTranslationData_1(package.classes, variants, locales) # .po data
            loc_dat = self._locale.getLocalizationData(locales)  # cldr data
            packageTranslations.append((pac_dat,loc_dat))
            if i18n_with_packages:
                package.data.translations.update(pac_dat)
                package.data.locales.update(loc_dat)

            self._console.outdent()

        self._console.outdent()
        return packageTranslations


    def generateLibInfoCode(self, libs, format, forceResourceUri=None, forceScriptUri=None):
        qxlibs = {}

        for lib in libs:
            # add library key
            qxlibs[lib['namespace']] = {}

            # add resource root URI
            if forceResourceUri:
                resUriRoot = forceResourceUri
            else:
                resUriRoot = self._computeResourceUri(lib, OsPath(""), rType="resource", appRoot=self.approot)
                resUriRoot = resUriRoot.encodedValue()
                
            qxlibs[lib['namespace']]['resourceUri'] = "%s" % (resUriRoot,)
            
            # add code root URI
            if forceScriptUri:
                sourceUriRoot = forceScriptUri
            else:
                sourceUriRoot = self._computeResourceUri(lib, OsPath(""), rType="class", appRoot=self.approot)
                sourceUriRoot = sourceUriRoot.encodedValue()
            
            qxlibs[lib['namespace']]['sourceUri'] = "%s" % (sourceUriRoot,)
            
            # TODO: Add version, svn revision, maybe even authors, but at least homepage link, ...

            # add version info
            if 'version' in lib:
                qxlibs[lib['namespace']]['version'] = "%s" % lib['version']

        return qxlibs


    def generateResourceInfoCode(self, script, settings, libs, format=False):
        """Pre-calculate image information (e.g. sizes)"""

        # some helper functions
        def replaceWithNamespace(imguri, liburi, libns):
            pre,libsfx,imgsfx = Path.getCommonPrefix(liburi, imguri)
            if imgsfx[0] == os.sep: imgsfx = imgsfx[1:]  # strip leading '/'
            imgshorturi = os.path.join("${%s}" % libns, imgsfx)
            return imgshorturi

        def extractAssetPart(libresuri, imguri):
            pre,libsfx,imgsfx = Path.getCommonPrefix(libresuri, imguri) # split libresuri from imguri
            if imgsfx[0] == os.sep: imgsfx = imgsfx[1:]  # strip leading '/'
            return imgsfx                # use the bare img suffix as its asset Id

        ##
        # calculate the uri of the clipped image, by taking the uri of the combined image,
        # "substracting" its asset id (the right end), taking what remains (the left
        # part), extracting the asset id of the clipped image, and pre-fixing it with the
        # left part of the combined image uri.
        # imageUri = (combinedUri - combinedAssetId) + imageAssetId
        #
        # @param uriFromMetafile |String| the path of the clipped image from when the meta file was generated,
        #                                 like: "./source/resource/qx/decoration/Modern/..."
        # @param trueCombinedUri |String| the uri of the combined image, as returned from
        #                                 the library scan and adapted for the current
        #                                 application, like: 
        #                                 "../../framework/source/resource/qx/decoration/Modern/panel-combined.png"
        # @param combinedUriFromMetafile |String| the path of the combined image, as
        #                                         recorded in the .meta file

        def normalizeImgUri(uriFromMetafile, trueCombinedUri, combinedUriFromMetafile):
            # normalize paths (esp. "./x" -> "x")
            (uriFromMetafile, trueCombinedUri, combinedUriFromMetafile) = map(os.path.normpath,
                                                    (uriFromMetafile, trueCombinedUri, combinedUriFromMetafile))
            # get the "wrong" left part of the combined image, as used in the .meta file (in mappedUriPrefix)
            trueUriPrefix, mappedUriPrefix, _ = Path.getCommonSuffix(trueCombinedUri, combinedUriFromMetafile)
            # ...and strip it from clipped image, to get a correct image id (in uriSuffix)
            _, _, uriSuffix = Path.getCommonPrefix(mappedUriPrefix, uriFromMetafile)
            # ...then compose the correct prefix with the correct suffix
            normalUri = os.path.normpath(os.path.join(trueUriPrefix, uriSuffix))
            return normalUri

        ##
        # - reads through the entries of a .meta file, which is the contents of a combined image
        # - for each contained image:
        #   - computes the image id ("short uri")
        #   - collects the list of interesting values (width, height, ..., combined image, ...)
        #   - and adds these as key:value to the general data map of images
        #
        # @param data |{imageId:[width, height, ...]}|  general map for qx.$$resource in loader
        # @param meta_fname |String| file path of the .meta file
        # @param combinedImageUri |String| uri of the combined image
        # @param combinedImageShortUri |String| short uri (image/asset id) of the combined image
        #                              these are necessary to compute the image id's of the contained imgs
        # @param combinedImageObject |ImgInfoFmt| an ImgInfoFmt wrapper object for the combined image
        #                             (interesting for the lib and type info)

        def processCombinedImg(script, data, meta_fname, combinedImageUri, combinedImageShortUri, combinedImageObject):
            # make sure lib and type info for the combined image are present
            assert combinedImageObject.lib, combinedImageObject.type

            # see if we have cached the contents (json) of this .meta file
            cacheId = "imgcomb-%s" % meta_fname
            imgDict = self._cache.read(cacheId, meta_fname)
            if imgDict == None:
                mfile = open(meta_fname)
                imgDict = simplejson.loads(mfile.read())
                mfile.close()
                self._cache.write(cacheId, imgDict)

            # now loop through the dict structure from the .meta file
            for imagePath, imageSpec_ in imgDict.items():
                # sort of like this: imagePath : [width, height, type, combinedUri, off-x, off-y]

                imageObject = ImgInfoFmt(imageSpec_) # turn this into an ImgInfoFmt object, to abstract from representation in .meta file and loader script

                # have to normalize the uri's from the meta file
                #imageUri = normalizeImgUri(imagePath, combinedImageUri, imageObject.mappedId)
                imageUri = imagePath

                ## replace lib uri with lib namespace in imageUri
                imageShortUri = extractAssetPart(librespath, imageUri)
                imageShortUri = Path.posifyPath(imageShortUri)

                # now put all elements of the image object together
                imageObject.mappedId = combinedImageShortUri        # correct the mapped uri of the combined image
                imageObject.lib      = combinedImageObject.lib
                imageObject.mtype    = combinedImageObject.type
                imageObject.mlib     = combinedImageObject.lib

                # and store it in the data structure
                imageFlat            = imageObject.flatten()  # this information takes precedence over existing
                data[imageShortUri]  = imageFlat
                addResourceToPackage(script, classToResourceMap, imageShortUri, imageFlat)

            return

        ##
        # finds the package that needs this resource <assetId> and adds it
        # TODO: this might be very expensive (lots of lookup's)

        def addResourceToPackage(script, classToResourceMap, assetId, resvalue):
            classesUsing = set(())
            for clazz, assetSet in classToResourceMap.items():
                for assetRex in assetSet:
                    if assetRex.match(assetId):
                        classesUsing.add(clazz)
                        break
            for package in script.packages:
                if classesUsing.intersection(set(package.classes)):
                    package.data.resources[assetId] = resvalue
            return


        # -- main --------------------------------------------------------------

        compConf = self._job.get("compile-options")
        compConf = ExtMap(compConf)
        resources_tree = compConf.get("code/resources-tree", False)
        
        resdata = {}
        if resources_tree:
            resdata = ExtMap()
        
        imgpatt  = re.compile(r'\.(png|jpeg|jpg|gif)$', re.I)
        skippatt = re.compile(r'\.(meta|py)$', re.I)

        self._console.info("Analyzing assets...")
        self._console.indent()

        self._imageInfo      = ImageInfo(self._console, self._cache)

        resourceFilter, classToResourceMap= self._resourceHandler.getResourceFilterByAssets(self._classList)

        # read img cache file
        cacheId = "imginfo-%s" % self._config._fname
        imgLookupTable = cache.read(cacheId, None)
        if imgLookupTable == None:
            imgLookupTable = {}

        for lib in libs:
            #libresuri = self._computeResourceUri(lib, "", rType='resource', appRoot=self.approot)
            librespath = os.path.normpath(os.path.join(lib['path'], lib['resource']))
            # TODO: scanning for resources should be handled in the LibraryPath class
            resourceList = self._resourceHandler.findAllResources([lib], resourceFilter)
            # resourceList = [[file1,uri1],[file2,uri2],...]
            for resource in resourceList:
                ##assetId = replaceWithNamespace(imguri, libresuri, lib['namespace'])
                #assetId = extractAssetPart(libresuri, resource[1])
                assetId = extractAssetPart(librespath,resource)
                assetId = Path.posifyPath(assetId)

                if imgpatt.search(resource): # handle images
                    imgpath= resource
                    #imguri = resource[1]
                    imguri = resource

                    # cache or generate
                    if (imgpath in imgLookupTable and
                        imgLookupTable[imgpath]["time"] > os.stat(imgpath).st_mtime):
                        imageInfo = imgLookupTable[imgpath]["content"]
                    else:
                        imageInfo = self._imageInfo.getImageInfo(imgpath, assetId)
                        imgLookupTable[imgpath] = {"time": time.time(), "content": imageInfo}

                    # use an ImgInfoFmt object, to abstract from flat format
                    imgfmt = ImgInfoFmt()
                    imgfmt.lib = lib['namespace']
                    if not 'type' in imageInfo:
                        raise RuntimeError, "Unable to get image info from file: %s" % imgpath
                    imgfmt.type = imageInfo['type']

                    # check for a combined image and process the contained images
                    meta_fname = os.path.splitext(imgpath)[0]+'.meta'
                    if os.path.exists(meta_fname):  # add included imgs
                        processCombinedImg(script, resdata, meta_fname, imguri, assetId, imgfmt)

                    # add this image directly
                    # imageInfo = {width, height, filetype}
                    if not 'width' in imageInfo or not 'height' in imageInfo:
                        raise RuntimeError, "Unable to get image info from file: %s" % imgpath
                    imgfmt.width, imgfmt.height, imgfmt.type = (
                        imageInfo['width'], imageInfo['height'], imageInfo['type'])
                    # check if img is already registered as part of a combined image
                    if assetId in resdata:
                        x = ImgInfoFmt()
                        x.fromFlat(resdata[assetId])
                        if x.mappedId:
                            continue  # don't overwrite the combined entry
                    resvalue = imgfmt.flatten()

                elif skippatt.search(resource[0]):
                    continue

                else:  # handle other resources
                    resvalue = lib['namespace']
                
                resdata[assetId] = resvalue
                addResourceToPackage(script, classToResourceMap, assetId, resvalue)  # register the resource with the package needing it


        # wpbasti: Image data is not part relevant yet.

        # write img cache file
        cache.write(cacheId, imgLookupTable)

        self._console.outdent()

        if resources_tree:
            resdata = resdata._data
        
        return resdata


    ##
    # returns the Javascript code for the initial ("boot") script as a string 

    def generateBootCode(self, parts, packages, boot, script, compConf, variants, settings, bootCode, globalCodes, version="source", decodeUrisFile=None, format=False):

        ##
        # create a map with part names as key and array of package id's and
        # return as string
        def partsMap(script):
            partData = {}
            packages = script.packagesSortedSimple()
            #print "packages: %r" % packages
            for part in script.parts:
                partData[part] = script.parts[part].packagesAsIndices(packages)
                #print "part '%s': %r" % (part, script.parts[part].packages)
            partData = json.dumpsCode(partData)

            return partData

        def fillTemplate(vals, template):
            # Fill the code template with various vals 
            templ  = MyTemplate(template)
            result = templ.safe_substitute(vals)

            return result

        def packageUrisToJS(packages, version, namespace=None):
            # Translate URI data to JavaScript
            
            allUris = []
            for packageId, package in enumerate(packages):
                packageUris = []
                for fileId in package:

                    if version == "build":
                        # TODO: gosh, the next is an ugly hack!
                        #namespace  = self._resourceHandler._genobj._namespaces[0]  # all name spaces point to the same paths in the libinfo struct, so any of them will do
                        if not namespace:
                            namespace  = self.getAppName()  # all name spaces point to the same paths in the libinfo struct, so any of them will do
                        relpath    = OsPath(fileId)
                    else:
                        namespace  = self._classes[fileId]["namespace"]
                        relpath    = OsPath(self._classes[fileId]["relpath"])

                    shortUri = Uri(relpath.toUri())
                    packageUris.append("%s:%s" % (namespace, shortUri.encodedValue()))
                allUris.append(packageUris)

            return allUris

        def packageUrisToJS1(packages, version, namespace=None):
            # Translate URI data to JavaScript
            # using Package objects

            if version == "build" and not namespace:
                # TODO: gosh, the next is an ugly hack!  
                # all name spaces point to the same paths in the libinfo struct, so any of them will do
                #namespace  = self._resourceHandler._genobj._namespaces[0]
                namespace  = self.getAppName()
            
            allUris = []
            for packageId, package in enumerate(packages):
                packageUris = []
                if package.file:
                    namespace = "__out__"
                    fileId    = package.file
                    relpath    = OsPath(fileId)
                    shortUri   = Uri(relpath.toUri())
                    packageUris.append("%s:%s" % (namespace, shortUri.encodedValue()))
                else: # "source" :
                    for clazz in package.classes:
                        namespace  = self._classes[clazz]["namespace"]
                        relpath    = OsPath(self._classes[clazz]["relpath"])
                        shortUri   = Uri(relpath.toUri())
                        packageUris.append("%s:%s" % (namespace, shortUri.encodedValue()))


                allUris.append(packageUris)
            return allUris

        def loadTemplate(bootCode):
            # try custom loader templates
            loaderFile = compConf.get("paths/loader-template", None)
            if not loaderFile:
                # use default templates
                if version=="build":
                    #loaderFile = os.path.join(filetool.root(), os.pardir, "data", "generator", "loader-build.tmpl.js")
                    # TODO: test-wise using generic template
                    loaderFile = os.path.join(filetool.root(), os.pardir, "data", "generator", "loader.tmpl.js")
                else:
                    #loaderFile = os.path.join(filetool.root(), os.pardir, "data", "generator", "loader-source.tmpl.js")
                    loaderFile = os.path.join(filetool.root(), os.pardir, "data", "generator", "loader.tmpl.js")
            
            template = filetool.read(loaderFile)

            return template

        # ---------------------------------------------------------------

        if not parts:
            return ""

        result           = ""
        vals             = {}
        packages         = script.packagesSortedSimple()
        loader_with_boot = self._job.get("packages/loader-with-boot", True)

        # stringify data in globalCodes
        for entry in globalCodes:
            globalCodes[entry] = json.dumpsCode(globalCodes[entry])
            # undo damage done by simplejson to raw strings with escapes \\ -> \
            globalCodes[entry] = globalCodes[entry].replace('\\\\\\', '\\').replace(r'\\', '\\')  # " gets tripple escaped, therefore the first .replace()

        vals.update(globalCodes)

        if version=="build":
            vals["Resources"] = json.dumpsCode({})  # TODO: undo Resources from globalCodes!!!
        vals["Boot"] = '"%s"' % boot
        if version == "build":
            vals["BootPart"] = bootCode
        else:
            vals["BootPart"] = ""
            # fake package data
            for key, package in enumerate(packages): 
                vals["BootPart"] += "qx.$$packageData['%d']={};\n" % key

        # Translate part information to JavaScript
        vals["Parts"] = partsMap(script)

        # Translate URI data to JavaScript
        #vals["Uris"] = packageUrisToJS(packages, version)
        vals["Uris"] = packageUrisToJS1(packages, version)
        vals["Uris"] = json.dumpsCode(vals["Uris"])

        # Add potential extra scripts
        vals["UrisBefore"] = []
        if self._job.get("add-script", False):
            additional_scripts = self._job.get("add-script",[])
            for additional_script in additional_scripts:
                vals["UrisBefore"].append(additional_script["uri"])
        vals["UrisBefore"] = json.dumpsCode(vals["UrisBefore"])

        # Whether boot package is inline
        if version == "source":
            vals["BootIsInline"] = json.dumpsCode(False)
        else:
            vals["BootIsInline"] = json.dumpsCode(loader_with_boot)
            
        # Closure package information
        cParts = {}
        if version == "build":
            for part in script.parts:
                if not loader_with_boot or part != "boot":
                    cParts[part] = True
        vals["ClosureParts"] = json.dumpsCode(cParts)

        # Package Hashes
        vals["PackageHashes"] = {}
        for key, package in enumerate(packages):
            if package.hash:
                vals["PackageHashes"][key] = package.hash
            else:
                vals["PackageHashes"][key] = "%d" % key  # fake code package hashes in source ver.
        vals["PackageHashes"] = json.dumpsCode(vals["PackageHashes"])

        # Script hook for qx.$$loader.decodeUris() function
        vals["DecodeUrisPlug"] = ""
        if decodeUrisFile:
            plugCode = filetool.read(self._config.absPath(decodeUrisFile))  # let it bomb if file can't be read
            vals["DecodeUrisPlug"] = plugCode.strip()
        
        # Locate and load loader basic script
        template = loadTemplate(bootCode)

        # Fill template gives result
        result = fillTemplate(vals, template)

        return result


    def packagesFileNames(self, basename, packagesLen, classPackagesOnly=False):
        loader_with_boot = self._job.get("packages/loader-with-boot", True)
        for packageId in range(packagesLen):
            suffix = packageId -1
            if suffix < 0:
                suffix = ""  # this is the loader package
                if (not loader_with_boot and classPackagesOnly):  # skip the loader package
                    continue
            packageFileName = self._resolveFileName(basename, self._variants, self._settings, suffix)
            yield packageFileName


    def writePackages1(self, compiledPackages, script, startId=0):
        for content, resolvedFilePath in zip(compiledPackages, self.packagesFileNames(script.baseScriptPath, len(compiledPackages))):
            # Save result file
            filetool.save(resolvedFilePath, content)

            if script.scriptCompress:
                filetool.gzip(resolvedFilePath, content)

            self._console.debug("Done: %s" % self._computeContentSize(content))
            self._console.debug("")

        return


    def writePackages(self, packages, script):

        for package in packages:
            filePath = package.file
            content = package.compiled
            self.writePackage(content, filePath, script)

        return

    
    def writePackage(self, content, filePath, script):
        if script.scriptCompress:
            filetool.gzip(filePath, content)
        else:
            filetool.save(filePath, content)


    ##
    # write 'Translations' and 'Locales' info out in dedicated files, so 
    # they don't blow up the loader; collect both translations and locales
    # info into a separate file for each locale code (e.g. 'en');
    # add URI information for the created files to globalCodes
    def writeI18NFiles(self, globalCodes, script):

        # for each locale code, collect mappings
        transKeys  = globalCodes['Translations'].keys()
        localeKeys = globalCodes['Locales'].keys()
        newParts   = {}    # language codes to part objects,    {"C": part}
        newPackages= {}    # language codes to private package objects, {"C": package}
        for localeCode in set(transKeys + localeKeys):
            # new: also provide a localeCode "part" with corresponding packages
            part = Part(localeCode)
            part.bit_mask = script.getPartBitMask()
            newParts[localeCode] = part
            package = Package(part.bit_mask)  # this might be modified later
            newPackages[localeCode] = package
            part.packages.append(package)

            data = {}
            data[localeCode] = { 'Translations': {}, 'Locales': {} }  # we want to have the locale code in the data
            if localeCode in transKeys:
                data[localeCode]['Translations']     = globalCodes['Translations'][localeCode]
                package.data.translations[localeCode] = globalCodes['Translations'][localeCode]
            if localeCode in localeKeys:
                data[localeCode]['Locales']     = globalCodes['Locales'][localeCode]
                package.data.locales[localeCode] = globalCodes['Locales'][localeCode]

            # write to file
            #dataS = json.dumpsCode(data)
            hash, dataS = package.packageContent()  # TODO: this currently works only for pure data packages
            dataS = dataS.replace('\\\\\\', '\\').replace(r'\\', '\\')  # undo damage done by simplejson to raw strings with escapes \\ -> \
            package.compiled = dataS
            fPath = self._resolveFileName(script.baseScriptPath, script.variants, script.settings, localeCode)
            self.writePackage(dataS, fPath, script)
            package.file = os.path.basename(fPath) # TODO: the use of os.path.basename is a hack
            package.hash = hash

        # Finalize the new packages and parts
        # - add prerequisite languages to parts; e.g. ["C", "en", "en_EN"]
        for partId, part in newParts.items():
            if newPackages["C"] not in part.packages:
                package = newPackages["C"]
                part.packages.append(package)   # all need "C"
                package.id |= part.bit_mask     # adapt package's bit string
            if len(partId) > 2 and partId[2] == "_":  # it's a sub-language -> include main language
                mainlang = partId[:2]
                if mainlang not in newPackages:
                    raise RuntimeError("Locale '%s' specified, but not base locale '%s'" % (partId, mainlang))
                if newPackages[mainlang] not in part.packages:
                    part.packages.append(newPackages[mainlang])   # add main language
                    newPackages[mainlang].id |= part.bit_mask     # adapt package's bit string

        # finally, sort packages
        for part in newParts.values():
            part.packagesSorted

        # - add to script object
        script.parts.update([(x.name, x) for x in newParts.values()])  # TODO: update might overwrite exist. entries!
        script.packages.extend(newPackages.values())

        return globalCodes


    def getAppName(self, memo={}):
        if not 'appname' in memo:
            appname = self._job.get("let/APPLICATION")
            if not appname:
                raise RuntimeError, "Need an application name in config (key let/APPLICATION)"
            else:
                memo['appname'] = appname
        return memo['appname']




# Helper class for string.Template, to overwrite the placeholder introducing delimiter
class MyTemplate(string.Template):
    delimiter = "%"

