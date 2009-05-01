<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"   
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
  xmlns:fn="http://www.w3.org/2005/xpath-functions" 
  xmlns:xdt="http://www.w3.org/2005/xpath-datatypes" 
  xmlns:gco="http://www.isotc211.org/2005/gco" 
  xmlns:gmd="http://www.isotc211.org/2005/gmd" 
  xmlns:xlink="http://www.w3.org/1999/xlink" 
  xmlns:gts="http://www.isotc211.org/2005/gts" 
  xmlns:gsr="http://www.isotc211.org/2005/gsr" 
  xmlns:gss="http://www.isotc211.org/2005/gss" 
  xmlns:gmx="http://www.isotc211.org/2005/gmx" 
  xmlns:gml="http://www.opengis.net/gml" 
  xsi:schemaLocation="http://www.isotc211.org/2005/gmd http://www.isotc211.org/2005/gmd/gmd.xsd"
  xmlns:func="http://exslt.org/functions"
  xmlns:exsl="http://exslt.org/common"
  xmlns:str="http://exslt.org/strings"
  xmlns:date="http://exslt.org/dates-and-times"
  xmlns:math="http://exslt.org/math"
  extension-element-prefixes="str func exsl date math">

  <xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes"/>
  <xsl:param name="language" select="'eng'"/>
  <xsl:param name="hierarchyLevel" select="'dataset'"/>
  <xsl:param name="themesListLocation" select="'http://asdd.ga.gov.au/asdd/profileinfo/anzlic-theme.xml'"/><!-- Change this to canonical location when available -->
  <xsl:param name="codesListLocation" select="'http://asdd.ga.gov.au/asdd/profileinfo/'"/><!-- Change this to canonical location when available -->
  <xsl:param name="metadataOrganisation" select="'metadataOrganisation'"/><!-- no default -->
  <xsl:param name="topicCategory"  select="'imageryBaseMapsEarthCover'"/>
  <xsl:param name="mdCreationDate" /><!-- no default -->
  <xsl:param name="resourceCreationDate" /><!-- no default -->
  <xsl:variable name="hierarchyLevelName">
    <xsl:choose><xsl:when test="$hierarchyLevel='dataset'">Dataset</xsl:when><xsl:otherwise><xsl:value-of select="$hierarchyLevel"/></xsl:otherwise></xsl:choose>
  </xsl:variable>
    
  <xsl:template match="/crawlresult">
    <gmd:MD_Metadata xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
                     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                     xmlns:fn="http://www.w3.org/2005/xpath-functions" 
                     xmlns:xdt="http://www.w3.org/2005/xpath-datatypes" 
                     xmlns:gco="http://www.isotc211.org/2005/gco" 
                     xmlns:gmd="http://www.isotc211.org/2005/gmd" 
                     xmlns:xlink="http://www.w3.org/1999/xlink" 
                     xmlns:gts="http://www.isotc211.org/2005/gts" 
                     xmlns:gsr="http://www.isotc211.org/2005/gsr" 
                     xmlns:gss="http://www.isotc211.org/2005/gss" 
                     xmlns:gmx="http://www.isotc211.org/2005/gmx" 
                     xmlns:gml="http://www.opengis.net/gml" 
                     xsi:schemaLocation="http://www.isotc211.org/2005/gmd http://www.isotc211.org/2005/gmd/gmd.xsd">

      <gmd:fileIdentifier>
        <gco:CharacterString><xsl:value-of select="guid"/></gco:CharacterString>
      </gmd:fileIdentifier>
      <gmd:language>
        <gco:CharacterString>eng</gco:CharacterString>
      </gmd:language>
      <gmd:characterSet>
        <gmd:MD_CharacterSetCode codeListValue="utf8" codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_CharacterSetCode"/>
      </gmd:characterSet>
      <gmd:parentIdentifier gco:nilReason="missing">
          <gco:CharacterString/>
      </gmd:parentIdentifier>
      <gmd:hierarchyLevel>
        <gmd:MD_ScopeCode>
          <xsl:attribute name="codeList">http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_ScopeCode</xsl:attribute>
          <xsl:attribute name="codeListValue"><xsl:value-of select="$hierarchyLevel"/></xsl:attribute>
        </gmd:MD_ScopeCode>
      </gmd:hierarchyLevel>
      <gmd:hierarchyLevelName>
        <gco:CharacterString><xsl:value-of select="$hierarchyLevelName"/></gco:CharacterString>
      </gmd:hierarchyLevelName>
      <xsl:call-template name="contact"/>
      <gmd:dateStamp>
          <gco:Date>
              <xsl:choose>
                  <xsl:when test="normalize-space(metadatadate)"><xsl:value-of select="metadatadate"/></xsl:when>
                  <xsl:otherwise><xsl:value-of select="date:format-date(date:date-time(),'yyyy-MM-dd')"/></xsl:otherwise>
              </xsl:choose>
          </gco:Date>
      </gmd:dateStamp>
      <gmd:metadataStandardName>
         <gco:CharacterString>ANZLIC Metadata Profile: An Australian/New Zealand Profile of AS/NZS ISO 19115:2005, Geographic information - Metadata</gco:CharacterString>
      </gmd:metadataStandardName>
      <gmd:metadataStandardVersion>
         <gco:CharacterString>1.1</gco:CharacterString>
      </gmd:metadataStandardVersion>
      
      <xsl:call-template name="referenceSystemInfo"/>
      <xsl:call-template name="metadataExtensionInfo"/>
      <xsl:call-template name="identificationInfo"/>
      <xsl:call-template name="contentInfo"/>
      <xsl:call-template name="distributionInfo"/>
      <xsl:call-template name="dataQualityInfo"/>
      <xsl:call-template name="metadataConstraints"/>

    </gmd:MD_Metadata>
  </xsl:template>

  <!--
    TOP LEVEL TEMPLATES
  -->
  <xsl:template name="contact">
      <xsl:choose>
          <xsl:when test="custodian">
            <xsl:call-template name="other_contact">
                <xsl:with-param name="contact" select="custodian"/>
            </xsl:call-template>
          </xsl:when>
          <xsl:otherwise>
            <gmd:contact>
              <xsl:call-template name="default_contact"/>
            </gmd:contact>
          </xsl:otherwise>
      </xsl:choose><!--/gmd:contact-->
      <xsl:if test="creator">
        <xsl:call-template name="other_contact">
          <xsl:with-param name="contact" select="creator"/>
        </xsl:call-template>
      </xsl:if>
      <xsl:if test="owner">
          <xsl:call-template name="other_contact">
              <xsl:with-param name="contact" select="owner"/>
          </xsl:call-template>
      </xsl:if>
  </xsl:template><!--contact-->
  <xsl:template name="default_contact">
    <xsl:param name="contact"><xsl:value-of select="'custodian'"/></xsl:param> <!--default-->
    <gmd:CI_ResponsibleParty>
      <gmd:organisationName>
        <gco:CharacterString>Australian Government Department of the Environment, Water, Heritage and the Arts</gco:CharacterString>
      </gmd:organisationName>
      <gmd:positionName>
        <gco:CharacterString>Remote Sensing Coordinator</gco:CharacterString>
      </gmd:positionName>
      <gmd:contactInfo>
        <gmd:CI_Contact>
             <gmd:phone>
                <gmd:CI_Telephone>
                   <gmd:voice>
                      <gco:CharacterString>+61 2 6275 9332</gco:CharacterString>
                   </gmd:voice>
                   <gmd:facsimile>
                      <gco:CharacterString>+ 61 2 6274 1333</gco:CharacterString>
                   </gmd:facsimile>
                </gmd:CI_Telephone>
             </gmd:phone>
             <gmd:address>
                <gmd:CI_Address>
                   <gmd:deliveryPoint>
                      <gco:CharacterString>GPO Box 787</gco:CharacterString>
                   </gmd:deliveryPoint>
                   <gmd:city>
                      <gco:CharacterString>Canberra</gco:CharacterString>
                   </gmd:city>
                   <gmd:administrativeArea>
                      <gco:CharacterString>Australian Captial Territory</gco:CharacterString>
                   </gmd:administrativeArea>
                   <gmd:postalCode>
                      <gco:CharacterString>2601</gco:CharacterString>
                   </gmd:postalCode>
                   <gmd:country>
                      <gco:CharacterString>Australia</gco:CharacterString>
                   </gmd:country>
                   <gmd:electronicMailAddress>
                      <gco:CharacterString>metadata@environment.gov.au</gco:CharacterString>
                   </gmd:electronicMailAddress>
                </gmd:CI_Address>
             </gmd:address>
             <gmd:onlineResource>
                <gmd:CI_OnlineResource>
                   <gmd:linkage>
                      <gmd:URL>http://www.environment.gov.au</gmd:URL>
                   </gmd:linkage>
                   <gmd:protocol>
                      <gco:CharacterString>WWW:LINK-1.0-http--link</gco:CharacterString>
                   </gmd:protocol>
                   <gmd:description>
                      <gco:CharacterString>image acquisitions</gco:CharacterString>
                   </gmd:description>
                </gmd:CI_OnlineResource>
             </gmd:onlineResource>
          </gmd:CI_Contact>
      </gmd:contactInfo>
      <gmd:role>
        <gmd:CI_RoleCode>
          <xsl:attribute name="codeList">http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_RoleCode</xsl:attribute>
          <xsl:attribute name="codeListValue"><xsl:value-of select="$contact"/></xsl:attribute>
        </gmd:CI_RoleCode>
      </gmd:role>
    </gmd:CI_ResponsibleParty>
  </xsl:template><!--default_custodian-->
  <xsl:template name="other_contact">
    <xsl:param name="contact"><xsl:value-of select="custodian"/></xsl:param> <!--default-->
    <xsl:variable name="tokens" select="str:tokenize(string($contact), '&#10;')"/>
    <gmd:contact>
      <gmd:CI_ResponsibleParty>
        <gmd:organisationName>
          <gco:CharacterString>
          <xsl:for-each select="$tokens">
            <xsl:variable name="token" select="str:tokenize(string(.), ':')"/>
            <xsl:if test="$token[1]='organisationName'"><xsl:value-of select="$token[2]"/></xsl:if>
          </xsl:for-each>
          </gco:CharacterString>
        </gmd:organisationName>
        <gmd:positionName>
          <gco:CharacterString>
            <xsl:for-each select="$tokens">
              <xsl:variable name="token" select="str:tokenize(string(.), ':')"/>
              <xsl:if test="$token[1]='positionName'"><xsl:value-of select="$token[2]"/></xsl:if>
            </xsl:for-each>
          </gco:CharacterString>
        </gmd:positionName>
        <gmd:contactInfo>
          <gmd:CI_Contact>
             <gmd:phone>
                <gmd:CI_Telephone>
                   <gmd:voice>
                     <gco:CharacterString>
                       <xsl:for-each select="$tokens">
                         <xsl:variable name="token" select="str:tokenize(string(.), ':')"/>
                         <xsl:if test="$token[1]='voice'"><xsl:value-of select="$token[2]"/></xsl:if>
                       </xsl:for-each>
                     </gco:CharacterString>
                   </gmd:voice>
                   <gmd:facsimile>
                     <gco:CharacterString>
                       <xsl:for-each select="$tokens">
                         <xsl:variable name="token" select="str:tokenize(string(.), ':')"/>
                         <xsl:if test="$token[1]='facsimile'"><xsl:value-of select="$token[2]"/></xsl:if>
                       </xsl:for-each>
                     </gco:CharacterString>
                   </gmd:facsimile>
                </gmd:CI_Telephone>
             </gmd:phone>
             <gmd:address>
               <gmd:CI_Address>
                 <gmd:deliveryPoint>
                   <gco:CharacterString>
                     <xsl:for-each select="$tokens">
                       <xsl:variable name="token" select="str:tokenize(string(.), ':')"/>
                       <xsl:if test="$token[1]='deliveryPoint'"><xsl:value-of select="$token[2]"/></xsl:if>
                     </xsl:for-each>
                   </gco:CharacterString>
                 </gmd:deliveryPoint>
                 <gmd:city>
                   <gco:CharacterString>
                     <xsl:for-each select="$tokens">
                       <xsl:variable name="token" select="str:tokenize(string(.), ':')"/>
                       <xsl:if test="$token[1]='city'"><xsl:value-of select="$token[2]"/></xsl:if>
                     </xsl:for-each>
                   </gco:CharacterString>
                 </gmd:city>
                 <gmd:administrativeArea>
                     <gco:CharacterString>
                         <xsl:for-each select="$tokens">
                             <xsl:variable name="token" select="str:tokenize(string(.), ':')"/>
                             <xsl:if test="$token[1]='administrativeArea'"><xsl:value-of select="$token[2]"/></xsl:if>
                         </xsl:for-each>
                     </gco:CharacterString>
                  </gmd:administrativeArea>
                  <gmd:postalCode>
                      <gco:CharacterString>
                          <xsl:for-each select="$tokens">
                              <xsl:variable name="token" select="str:tokenize(string(.), ':')"/>
                              <xsl:if test="$token[1]='postalCode'"><xsl:value-of select="$token[2]"/></xsl:if>
                          </xsl:for-each>
                      </gco:CharacterString>
                  </gmd:postalCode>
                  <gmd:country>
                    <gco:CharacterString>
                      <xsl:for-each select="$tokens">
                        <xsl:variable name="token" select="str:tokenize(string(.), ':')"/>
                        <xsl:if test="$token[1]='country'"><xsl:value-of select="$token[2]"/></xsl:if>
                      </xsl:for-each>
                    </gco:CharacterString>
                  </gmd:country>
                  <gmd:electronicMailAddress>
                    <gco:CharacterString>
                      <xsl:for-each select="$tokens">
                        <xsl:variable name="token" select="str:tokenize(string(.), ':')"/>
                        <xsl:if test="$token[1]='electronicMailAddress'"><xsl:value-of select="$token[2]"/></xsl:if>
                      </xsl:for-each>
                    </gco:CharacterString>
                  </gmd:electronicMailAddress>
                </gmd:CI_Address>
             </gmd:address>
          </gmd:CI_Contact>
        </gmd:contactInfo>
        <gmd:role>
          <gmd:CI_RoleCode>
            <xsl:attribute name="codeList">http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_RoleCode</xsl:attribute>
            <xsl:attribute name="codeListValue"><xsl:value-of select="local-name($contact)"/></xsl:attribute>
          </gmd:CI_RoleCode>
        </gmd:role>
      </gmd:CI_ResponsibleParty>
    </gmd:contact>
  </xsl:template><!--other_contact--> 
  <!--
  -->  
  <xsl:template name="referenceSystemInfo">
    <xsl:if test="normalize-space(srs)">
      <gmd:referenceSystemInfo>
        <gmd:MD_ReferenceSystem>
          <gmd:referenceSystemIdentifier>
            <gmd:RS_Identifier>
              <gmd:authority>
                <gmd:CI_Citation>
                <xsl:variable name="rs_type">
                  <xsl:choose>
                    <xsl:when test="not(normalize-space(epsg))">OGC</xsl:when>
                    <xsl:when test="normalize-space(epsg) = '0'">OGC</xsl:when>
                    <xsl:otherwise>EPSG</xsl:otherwise>
                  </xsl:choose>
                </xsl:variable>
                <gmd:title>
                  <gco:CharacterString>
                  <xsl:choose>
                    <xsl:when test="$rs_type='OGC'">
                    <xsl:value-of select="'OGC Well-known Text Representation of Spatial Reference Systems'"/>
                    </xsl:when>
                    <xsl:otherwise>
                    <xsl:value-of select="'EPSG Geodetic Parameter Dataset'"/>
                    </xsl:otherwise>
                  </xsl:choose>
                  </gco:CharacterString>
                </gmd:title>
                <gmd:date>
                  <gmd:CI_Date>
                  <gmd:date>
                    <xsl:choose>
                    <xsl:when test="$rs_type='OGC'">
                      <gco:Date>2006-10-05</gco:Date>
                    </xsl:when>
                    <xsl:otherwise>
                      <gco:Date>2007-07-16</gco:Date>
                    </xsl:otherwise>
                    </xsl:choose>
                  </gmd:date>
                  <gmd:dateType>
                    <gmd:CI_DateTypeCode>
                    <xsl:attribute name="codeList">http://www.isotc211.org/2005/resources/Codelist/gmxCodelist.xml#CI_DateTypeCode</xsl:attribute>
                    <xsl:attribute name="codeListValue">revision</xsl:attribute>
                    </gmd:CI_DateTypeCode>
                  </gmd:dateType>
                  </gmd:CI_Date>
                </gmd:date>
                <gmd:edition>
                  <xsl:choose>
                  <xsl:when test="$rs_type='OGC'">
                    <gco:CharacterString>Version 1.20</gco:CharacterString>
                  </xsl:when>
                  <xsl:otherwise>
                    <gco:CharacterString>Version 6.13</gco:CharacterString>
                  </xsl:otherwise>
                  </xsl:choose>
                </gmd:edition>
                </gmd:CI_Citation>
              </gmd:authority>
              <gmd:code>
                <gco:CharacterString>
                  <xsl:choose>
                  <xsl:when test="not(normalize-space(epsg))">
                    <xsl:value-of select="srs"/>
                  </xsl:when>
                  <xsl:when test="normalize-space(epsg) = '0'">
                    <xsl:value-of select="srs"/>
                  </xsl:when>
                  <xsl:otherwise>
                    <xsl:value-of select="epsg"/>
                  </xsl:otherwise>
                  </xsl:choose>
                </gco:CharacterString>
              </gmd:code>
            </gmd:RS_Identifier>
          </gmd:referenceSystemIdentifier>
        </gmd:MD_ReferenceSystem>
      </gmd:referenceSystemInfo>
    </xsl:if>
  </xsl:template> <!--referenceSystemInfo-->
  <!--
  -->  
  <xsl:template name="metadataExtensionInfo">
    <gmd:metadataExtensionInfo>
      <gmd:MD_MetadataExtensionInformation/>
    </gmd:metadataExtensionInfo>
  </xsl:template><!--metadataExtensionInfo-->  
  <!--
  -->  
  <xsl:template name="identificationInfo">
      <gmd:identificationInfo>
        <gmd:MD_DataIdentification>
          <gmd:citation>
            <gmd:CI_Citation>
              <gmd:title>
                <gco:CharacterString>
                  <xsl:choose>
                    <xsl:when test="title">
                      <xsl:value-of select="normalize-space(title)"/>
                    </xsl:when>
                    <xsl:otherwise>
                      <xsl:value-of select="'PLEASE ENTER A TITLE! File name = '"/>
                      <xsl:value-of select="filename"/>
                    </xsl:otherwise>
                  </xsl:choose>
                </gco:CharacterString>
              </gmd:title>
              <gmd:date>
                <gmd:CI_Date>
                  <gmd:date>
                    <gco:Date>
                      <xsl:choose>
                        <xsl:when test="normalize-space(imgdate)"><xsl:value-of select="imgdate"/></xsl:when>
                        <xsl:otherwise><xsl:value-of select="date:format-date(date:date-time(),'yyyy-MM-dd')"/></xsl:otherwise>
                      </xsl:choose>
                    </gco:Date>
                  </gmd:date>            
                  <gmd:dateType>
                    <gmd:CI_DateTypeCode codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_DateTypeCode" codeListValue="creation">
                      <xsl:value-of select="'creation'"/>
                    </gmd:CI_DateTypeCode>
                  </gmd:dateType>
                </gmd:CI_Date>
              </gmd:date>
              <gmd:identifier>
                <gmd:MD_Identifier>
                  <gmd:authority>
                    <gmd:CI_Citation>
                      <gmd:title>
                        <gco:CharacterString>ANZLIC Identifier</gco:CharacterString>
                      </gmd:title>
                      <gmd:date>
                        <gmd:CI_Date>
                          <gmd:date>
                            <gco:Date>2001-02</gco:Date>
                          </gmd:date>
                          <gmd:dateType>
                            <gmd:CI_DateTypeCode codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_DateTypeCode" codeListValue="revision">
                              <xsl:value-of select="'revision'"/>
                            </gmd:CI_DateTypeCode>
                          </gmd:dateType>
                        </gmd:CI_Date>
                      </gmd:date>
                      <gmd:edition>
                        <gco:CharacterString>Version 2</gco:CharacterString>
                      </gmd:edition>
                      <gmd:editionDate>
                        <gco:Date>2001-02</gco:Date>
                      </gmd:editionDate>
                      <gmd:citedResponsibleParty>
                        <gmd:CI_ResponsibleParty>
                          <gmd:organisationName>
                            <gco:CharacterString>ANZLIC - the Spatial Information Council</gco:CharacterString>
                          </gmd:organisationName>
                          <gmd:role>
                            <gmd:CI_RoleCode codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_RoleCode" codeListValue="owner">
                              <xsl:value-of select="'owner'"/>
                            </gmd:CI_RoleCode>
                          </gmd:role>
                        </gmd:CI_ResponsibleParty>
                      </gmd:citedResponsibleParty>
                      <gmd:otherCitationDetails>
                        <gco:CharacterString>Defined in ANZLIC Metadata Guidelines Version 2 http://www.anzlic.org.au/download.html?oid=2358011755</gco:CharacterString>
                      </gmd:otherCitationDetails>
                    </gmd:CI_Citation>
                  </gmd:authority>
                  <gmd:code>
                    <gco:CharacterString>
                      <xsl:value-of select="guid"/>
                    </gco:CharacterString>
                  </gmd:code>
                </gmd:MD_Identifier>
              </gmd:identifier>
            </gmd:CI_Citation>
          </gmd:citation>
          <gmd:abstract>
            <gco:CharacterString>
              <xsl:choose>
                <xsl:when test="abstract">
                  <xsl:value-of select="normalize-space(abstract)"/>
                </xsl:when>
                <xsl:otherwise>
                  <xsl:value-of select="'PLEASE ENTER AN ABSTRACT!'"/>
                </xsl:otherwise>
              </xsl:choose>
            </gco:CharacterString>
          </gmd:abstract>
          <gmd:status>
            <gmd:MD_ProgressCode 
                codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_ProgressCode"
                codeListValue="completed"/>
          </gmd:status>
          <gmd:resourceMaintenance>
            <gmd:MD_MaintenanceInformation>
              <gmd:maintenanceAndUpdateFrequency>
                <gmd:MD_MaintenanceFrequencyCode 
                    codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_MaintenanceFrequencyCode"
                    codeListValue="notPlanned"/>
              </gmd:maintenanceAndUpdateFrequency>
            </gmd:MD_MaintenanceInformation>
          </gmd:resourceMaintenance>
          <gmd:resourceFormat>
            <gmd:MD_Format>
              <gmd:name>
                <gco:CharacterString>
                  <xsl:value-of select="normalize-space(filetype)"/>
                </gco:CharacterString>
              </gmd:name>
              <gmd:version>
                <gco:CharacterString>none</gco:CharacterString>
              </gmd:version>
            </gmd:MD_Format>
          </gmd:resourceFormat>
          <gmd:descriptiveKeywords>
            <gmd:MD_Keywords>
              <gmd:keyword>
                <gco:CharacterString>imageryBaseMapsEarthCover</gco:CharacterString>
              </gmd:keyword>    
              <gmd:type>
                <gmd:MD_KeywordTypeCode 
                    codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_KeywordTypeCode"
                    codeListValue="discipline">
                  <xsl:value-of select="'discipline'"/>
                </gmd:MD_KeywordTypeCode>
              </gmd:type>
              <gmd:thesaurusName>
                <gmd:CI_Citation>
                  <gmd:title>
                    <gco:CharacterString>ANZLIC Search Words</gco:CharacterString>
                  </gmd:title>
                  <gmd:date>
                    <gmd:CI_Date>
                      <gmd:date>
                        <gco:Date>2001</gco:Date>
                      </gmd:date>
                      <gmd:dateType>
                        <gmd:CI_DateTypeCode codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_DateTypeCode" codeListValue="revision">
                          <xsl:value-of select="'revision'"/>
                        </gmd:CI_DateTypeCode>
                      </gmd:dateType>
                    </gmd:CI_Date>
                  </gmd:date>
                  <gmd:edition>
                    <gco:CharacterString>Version 2</gco:CharacterString>
                  </gmd:edition>
                  <gmd:editionDate>
                    <gco:Date>2001-02</gco:Date>
                  </gmd:editionDate>
                  <gmd:identifier>
                    <gmd:MD_Identifier>
                      <gmd:code>
                        <gco:CharacterString><xsl:value-of select="$themesListLocation"/></gco:CharacterString>
                      </gmd:code>
                    </gmd:MD_Identifier>
                  </gmd:identifier>
                  <gmd:citedResponsibleParty>
                    <gmd:CI_ResponsibleParty>
                      <gmd:organisationName>
                        <gco:CharacterString>ANZLIC - the Spatial Information Council</gco:CharacterString>
                      </gmd:organisationName>
                      <gmd:role>
                        <gmd:CI_RoleCode 
                            codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_RoleCode"
                            codeListValue="custodian">
                          <xsl:value-of select="'custodian'"/>
                        </gmd:CI_RoleCode>
                      </gmd:role>
                    </gmd:CI_ResponsibleParty>
                  </gmd:citedResponsibleParty>
                </gmd:CI_Citation>
              </gmd:thesaurusName>
            </gmd:MD_Keywords>
          </gmd:descriptiveKeywords>
          <gmd:resourceConstraints>
            <gmd:MD_Constraints>
              <gmd:useLimitation>
                <gco:CharacterString>PLEASE ENTER ANY ACCESS CONSTRAINTS!</gco:CharacterString>
              </gmd:useLimitation>
            </gmd:MD_Constraints>
          </gmd:resourceConstraints>
          <gmd:spatialResolution>
            <gmd:MD_Resolution>
              <gmd:distance>
                <gco:Distance>
                  <xsl:attribute name="uom"><xsl:value-of select="units"/></xsl:attribute>
                  <xsl:value-of select="str:split(cellx,',')[1]"/>
                  <!--xsl:value-of select="cellx"/--> <!--cellx can have multiple values (e.g. ASTER & ALI) so just pick the first 1-->
                </gco:Distance>
              </gmd:distance>
            </gmd:MD_Resolution>
          </gmd:spatialResolution>
          <gmd:spatialResolution>
            <gmd:MD_Resolution>
              <gmd:distance>
                <gco:Distance>
                  <xsl:attribute name="uom"><xsl:value-of select="units"/></xsl:attribute>
                  <xsl:value-of select="str:split(celly,',')[1]"/>
                  <!--xsl:value-of select="celly"/--> <!--cellx can have multiple values (e.g. ASTER & ALI) so just pick the first 1-->
                </gco:Distance>
              </gmd:distance>
            </gmd:MD_Resolution>
          </gmd:spatialResolution>
          <gmd:language>
            <gco:CharacterString><xsl:value-of select="$language"/></gco:CharacterString>
          </gmd:language>
          <gmd:topicCategory>
            <gmd:MD_TopicCategoryCode><xsl:value-of select="$topicCategory"/></gmd:MD_TopicCategoryCode>
          </gmd:topicCategory>
          <gmd:extent>
            <gmd:EX_Extent>
              <gmd:geographicElement>
                <xsl:variable name="xmin">
                  <xsl:copy-of select="str:split(UL,',')[1]"/>
                  <xsl:copy-of select="str:split(LL,',')[1]"/>
                </xsl:variable>
                <xsl:variable name="ymin">
                  <xsl:copy-of select="str:split(LR,',')[2]"/>
                  <xsl:copy-of select="str:split(LL,',')[2]"/>
                </xsl:variable>
                <xsl:variable name="xmax">
                  <xsl:copy-of select="str:split(UR,',')[1]"/>
                  <xsl:copy-of select="str:split(LR,',')[1]"/>
                </xsl:variable>
                <xsl:variable name="ymax">
                  <xsl:copy-of select="str:split(UR,',')[2]"/>
                  <xsl:copy-of select="str:split(UL,',')[2]"/>
                </xsl:variable>
                <gmd:EX_GeographicBoundingBox>
                  <gmd:extentTypeCode>
                    <gco:Boolean>1</gco:Boolean>
                  </gmd:extentTypeCode>
                  <gmd:westBoundLongitude>
                    <gco:Decimal><xsl:value-of select="math:min(exsl:node-set($xmin)/*)"/></gco:Decimal>
                  </gmd:westBoundLongitude>
                  <gmd:eastBoundLongitude>
                    <gco:Decimal><xsl:value-of select="math:max(exsl:node-set($xmax)/*)"/></gco:Decimal>
                  </gmd:eastBoundLongitude>
                  <gmd:southBoundLatitude>
                    <gco:Decimal><xsl:value-of select="math:min(exsl:node-set($ymin)/*)"/></gco:Decimal>
                  </gmd:southBoundLatitude>
                  <gmd:northBoundLatitude>
                    <gco:Decimal><xsl:value-of select="math:max(exsl:node-set($ymax)/*)"/></gco:Decimal>
                  </gmd:northBoundLatitude>
                </gmd:EX_GeographicBoundingBox>
              </gmd:geographicElement>
              <gmd:geographicElement>
                <gmd:EX_BoundingPolygon>
                  <gmd:polygon>
                    <gml:Polygon gml:id="BP01">
                      <gml:exterior> 
                        <gml:LinearRing>
                          <gml:pos><xsl:value-of select="str:replace(LL, ',', ' ')"/></gml:pos>
                          <gml:pos><xsl:value-of select="str:replace(UL, ',', ' ')"/></gml:pos>
                          <gml:pos><xsl:value-of select="str:replace(UR, ',', ' ')"/></gml:pos>
                          <gml:pos><xsl:value-of select="str:replace(LR, ',', ' ')"/></gml:pos>
                        </gml:LinearRing>
                      </gml:exterior>
                    </gml:Polygon>
                  </gmd:polygon>
                </gmd:EX_BoundingPolygon>
              </gmd:geographicElement>
              <gmd:geographicElement>
                <gmd:EX_GeographicDescription>
                  <gmd:geographicIdentifier>
                    <gmd:MD_Identifier>
                      <gmd:authority>
                        <gmd:CI_Citation>
                          <gmd:title>
                            <gco:CharacterString>ANZLIC Geographic Extent Name Register - States and Territories</gco:CharacterString>
                          </gmd:title>
                          <gmd:date>
                            <gmd:CI_Date>
                              <gmd:date>
                                <gco:Date>2003-12-10</gco:Date>
                              </gmd:date>
                              <gmd:dateType>
                                <gmd:CI_DateTypeCode codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_DateTypeCode"
                                                       codeListValue="creation"/>
                              </gmd:dateType>
                            </gmd:CI_Date>
                          </gmd:date>
                          <gmd:date>
                            <gmd:CI_Date>
                              <gmd:date>
                                <gco:Date>2003-12-10</gco:Date>
                              </gmd:date>
                              <gmd:dateType>
                                <gmd:CI_DateTypeCode codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_DateTypeCode"
                                                     codeListValue="revision"/>
                              </gmd:dateType>
                            </gmd:CI_Date>
                          </gmd:date>
                          <gmd:edition>
                            <gco:CharacterString>1</gco:CharacterString>
                          </gmd:edition>
                          <gmd:identifier>
                            <gmd:MD_Identifier>
                               <gmd:code>
                                  <gco:CharacterString>http://www.ga.gov.au/anzmeta/gen/anzlic-algens.xml#anzlic-state_territory</gco:CharacterString>
                               </gmd:code>
                            </gmd:MD_Identifier>
                          </gmd:identifier>
                          <gmd:citedResponsibleParty xlink:href="www.environment.gov.au"/>
                          <gmd:presentationForm>
                            <gmd:CI_PresentationFormCode codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_PresentationFormCode"
                                                         codeListValue="documentDigital"/>
                          </gmd:presentationForm>
                        </gmd:CI_Citation>
                      </gmd:authority>
                      <gmd:code>
                        <gco:CharacterString>AUSTRALIA EXCLUDING EXTERNAL TERRITORIES</gco:CharacterString>
                      </gmd:code>
                    </gmd:MD_Identifier>
                  </gmd:geographicIdentifier>
                </gmd:EX_GeographicDescription>
              </gmd:geographicElement>
              <gmd:temporalElement>
                <gmd:EX_TemporalExtent>
                  <gmd:extent>
                    <gml:TimePeriod gml:id="TP01">
                      <gml:beginPosition>
                        <xsl:choose>
                          <xsl:when test="normalize-space(imgdate)">
                            <xsl:value-of select="imgdate"/>
                          </xsl:when>
                          <xsl:otherwise>
                            <xsl:attribute name="indeterminatePosition">unknown</xsl:attribute>
                          </xsl:otherwise>
                        </xsl:choose>
                      </gml:beginPosition>
                      <gml:endPosition>
                        <xsl:choose>
                          <xsl:when test="normalize-space(imgdate)">
                            <xsl:value-of select="imgdate"/>
                          </xsl:when>
                          <xsl:otherwise>
                            <xsl:attribute name="indeterminatePosition">unknown</xsl:attribute>
                          </xsl:otherwise>
                        </xsl:choose>
                      </gml:endPosition>
                    </gml:TimePeriod>
                  </gmd:extent>
                </gmd:EX_TemporalExtent>
              </gmd:temporalElement>
            </gmd:EX_Extent>
          </gmd:extent>
          <gmd:supplementalInformation>
            <gco:CharacterString>
              <xsl:for-each select="./*">
                <xsl:value-of select="local-name(.)"/>: <xsl:value-of select="."/>
                <xsl:if test="position() != last()">  |  </xsl:if>
              </xsl:for-each>
            </gco:CharacterString>
          </gmd:supplementalInformation>
        </gmd:MD_DataIdentification>
      </gmd:identificationInfo>
  </xsl:template><!--identificationInfo--> 
  <!--
  -->  
  <xsl:template name="contentInfo">
    <xsl:variable name="tbands" select="str:tokenize(string(bands), ',')"/>
    <xsl:variable name="tnbits" select="str:tokenize(string(nbits), ',')"/>
    <xsl:variable name="tnodata" select="str:tokenize(string(nodata), ',')"/>
    <xsl:variable name="trows" select="str:tokenize(string(rows), ',')"/>
    <xsl:variable name="tcols" select="str:tokenize(string(cols), ',')"/>
    <xsl:variable name="tcellx" select="str:tokenize(string(cellx), ',')"/>
    <xsl:variable name="tcelly" select="str:tokenize(string(celly), ',')"/>
    <xsl:variable name="tdatatype" select="str:tokenize(string(celly), ',')"/>
    <xsl:variable name="tbandcount" select="count($tbands)"/>
    
    <gmd:contentInfo>
      <gmd:MD_ImageDescription>
        <gmd:attributeDescription>
          <gco:RecordType/>
        </gmd:attributeDescription>
        <gmd:contentType>
          <gmd:MD_CoverageContentTypeCode codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_CoverageContentTypeCode"
                                          codeListValue="image"/>
        </gmd:contentType>
        <xsl:call-template name="bands">
          <xsl:with-param name="band" select="1"/>
          <xsl:with-param name="count" select="$tbandcount"/>
          <xsl:with-param name="tbands" select="$tbands"/>
          <xsl:with-param name="tnbits" select="$tnbits"/>
        </xsl:call-template>

        <xsl:if test="normalize-space(sunelevation)">
          <gmd:illuminationElevationAngle>
            <gco:Real><xsl:value-of select="normalize-space(sunelevation)"/></gco:Real>
          </gmd:illuminationElevationAngle>
        </xsl:if>
        <xsl:if test="normalize-space(sunazimuth)">
          <gmd:illuminationAzimuthAngle>
            <gco:Real><xsl:value-of select="normalize-space(sunazimuth)"/></gco:Real>
          </gmd:illuminationAzimuthAngle>
        </xsl:if>
        <xsl:if test="normalize-space(cloudcover)">
          <gmd:imagingCondition>
            <gmd:MD_ImagingConditionCode 
                codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_ImagingConditionCode"
                codeListValue="cloud"/>
          </gmd:imagingCondition>
          <gmd:imageQualityCode>
            <!--gmd:RS_Identifier--> <!-- MD or RS Not sure about this... -->
            <gmd:MD_Identifier>
              <gmd:code gco:nilReason="missing">
                <gco:CharacterString/>
              </gmd:code>
            </gmd:MD_Identifier>
            <!--/gmd:RS_Identifier--> <!-- MD or RS Not sure about this... -->
          </gmd:imageQualityCode>
          <gmd:cloudCoverPercentage>
            <gco:Real><xsl:value-of select="normalize-space(cloudcover)"/></gco:Real>
          </gmd:cloudCoverPercentage>
        </xsl:if>
        <xsl:if test="normalize-space(level)">
          <gmd:processingLevelCode>
            <gmd:MD_Identifier>
              <gmd:code>
                <gco:CharacterString><xsl:value-of select="normalize-space(level)"/></gco:CharacterString>
              </gmd:code>
            </gmd:MD_Identifier>
          </gmd:processingLevelCode>
        </xsl:if>
        <!-- leave these in case we do something with them in the future -->
        <xsl:if test="normalize-space(radiometricCalibrationDataAvailability)">
          <gmd:radiometricCalibrationDataAvailability>
            <gco:Boolean>1</gco:Boolean>
          </gmd:radiometricCalibrationDataAvailability>
        </xsl:if>
        <xsl:if test="normalize-space(cameraCalibrationInformationAvailability)">
          <gmd:cameraCalibrationInformationAvailability>
            <gco:Boolean>0</gco:Boolean>
          </gmd:cameraCalibrationInformationAvailability>
        </xsl:if>
        <xsl:if test="normalize-space(filmDistortionInformationAvailability)">
          <gmd:filmDistortionInformationAvailability>
            <gco:Boolean>1</gco:Boolean>
          </gmd:filmDistortionInformationAvailability>
        </xsl:if>
        <xsl:if test="normalize-space(lensDistortionInformationAvailability)">
          <gmd:lensDistortionInformationAvailability>
           <gco:Boolean>1</gco:Boolean>
          </gmd:lensDistortionInformationAvailability>
        </xsl:if>
      </gmd:MD_ImageDescription>
    </gmd:contentInfo>
  </xsl:template><!--contentInfo-->
  <xsl:template name="bands">
    <xsl:param name="band"  select="'1'"/>
    <xsl:param name="count" select="'1'"/>
    <xsl:param name="tbands"/>
    <xsl:param name="tnbits"/>
    <!--xsl:param name="tnodata"/-->
    <!--xsl:param name="trows"/-->
    <!--xsl:param name="tcols"/-->
    <!--xsl:param name="tcellx"/-->
    <!--xsl:param name="tcelly"/-->
    <!--xsl:param name="tdatatype"/-->
      <xsl:if test="$band &lt;= $count">
        <gmd:dimension>
          <gmd:MD_Band>
            <gmd:descriptor>
              <xsl:choose>
                <xsl:when test="normalize-space($tbands[$band])">
                  <gco:CharacterString><xsl:value-of select="$tbands[$band]"/></gco:CharacterString>
                </xsl:when>
                <xsl:otherwise>
                  <gco:CharacterString><xsl:value-of select="$band"/></gco:CharacterString>
                </xsl:otherwise>
              </xsl:choose>
            </gmd:descriptor>
            <gmd:bitsPerValue>
              <xsl:choose>
                <xsl:when test="normalize-space($tnbits[$band])">
                  <gco:Integer><xsl:value-of select="floor($tnbits[$band])"/></gco:Integer>
                </xsl:when>
                <xsl:otherwise>
                  <gco:Integer><xsl:value-of select="floor($tnbits[1])"/></gco:Integer>
                </xsl:otherwise>
              </xsl:choose>
            </gmd:bitsPerValue>
          </gmd:MD_Band>
        </gmd:dimension>
        <xsl:call-template name="bands">
          <xsl:with-param name="band" select="$band + 1"/>
          <xsl:with-param name="count" select="$count"/>
          <xsl:with-param name="tbands" select="$tbands"/>
          <xsl:with-param name="tnbits" select="$tnbits"/>
        </xsl:call-template>
      </xsl:if>
  </xsl:template><!--bands-->
  <!--
  -->  
  <xsl:template name="distributionInfo">
    <gmd:distributionInfo>
      <gmd:MD_Distribution>
        <gmd:distributionFormat>
          <gmd:MD_Format>
            <gmd:name>
              <gco:CharacterString><xsl:value-of select="filetype"/></gco:CharacterString>
            </gmd:name>
            <gmd:version>
              <gco:CharacterString>1</gco:CharacterString>
            </gmd:version>
          </gmd:MD_Format>
        </gmd:distributionFormat>
        <gmd:distributor>
          <gmd:MD_Distributor>
            <gmd:distributorContact>
              <xsl:call-template name="default_contact">
                <xsl:with-param name="contact" select="'distributor'"/>
              </xsl:call-template>
            </gmd:distributorContact>
            </gmd:MD_Distributor>
        </gmd:distributor>
        <!-- Commented out for future use. 
              NOTE: remove underscores between the dashes from 
              WWW:LINK-1.0-http-_- etc... they were added to workaround comment character issues with the parser
        -->  
        <!--gmd:transferOptions>
          <gmd:MD_DigitalTransferOptions>
            <gmd:onLine>
              <gmd:CI_OnlineResource>
                <gmd:linkage>
                  <gmd:URL>http://pandora:81/ecwp/ecw_wms.dll?000014?Request=GetCapabilities</gmd:URL>
                </gmd:linkage>
                <gmd:protocol>
                  <gco:CharacterString>OGC:WMS-1.1.1-http-get-map</gco:CharacterString>
                </gmd:protocol>
                <gmd:description>
                  <gco:CharacterString>Image Web Server Web Map Service</gco:CharacterString>
                </gmd:description>
              </gmd:CI_OnlineResource>
            </gmd:onLine>
            <gmd:onLine>
              <gmd:CI_OnlineResource>
                <gmd:linkage>
                  <gmd:URL>http://pandora:81/ecwp/ImageX.dll?image?layers=/iwsimages/aus/aust_2004.ecw&amp;sizex=800&amp;sizey=800&amp;quality=80&amp;type=png</gmd:URL>
                </gmd:linkage>
                <gmd:protocol>
                  <gco:CharacterString>WWW:LINK-1.0-http- -link</gco:CharacterString>
                </gmd:protocol>
                <gmd:name>
                  <gco:CharacterString>Image Web Server Image X</gco:CharacterString>
                </gmd:name>
                <gmd:description>
                  <gco:CharacterString>Image Web Server Image X (simple browser display)</gco:CharacterString>
                </gmd:description>
              </gmd:CI_OnlineResource>
            </gmd:onLine>
            <gmd:onLine>
              <gmd:CI_OnlineResource>
                <gmd:linkage>
                  <gmd:URL>http://pandora:81/ecwp/ecw_wms.dll?000014?SERVICE=WMS&amp;VERSION=1.1.1&amp;REQUEST=GetMap&amp;LAYERS=AUST_2004.ECW&amp;SRS=EPSG:4326&amp;BBOX=100.0,0,180.0,-60.0&amp;WIDTH=800&amp;HEIGHT=600&amp;FORMAT=image/png&amp;TRANSPARENT=TRUE&amp;STYLES=raster</gmd:URL>
                </gmd:linkage>
                <gmd:protocol>
                  <gco:CharacterString>WWW:LINK-1.0-http- -link</gco:CharacterString>
                </gmd:protocol>
                <gmd:name>
                  <gco:CharacterString>Image Web Server WMS GetMap</gco:CharacterString>
                </gmd:name>
                <gmd:description>
                  <gco:CharacterString>Image Web Server WMS GetMap image display</gco:CharacterString>
                </gmd:description>
              </gmd:CI_OnlineResource>
            </gmd:onLine>
            <gmd:onLine>
              <gmd:CI_OnlineResource>
                <gmd:linkage>
                  <gmd:URL>http://pandora.internal.govt:81/tmp/000014.kml</gmd:URL>
                </gmd:linkage>
                <gmd:protocol>
                  <gco:CharacterString>GLG:KML-2.0-http-get-map</gco:CharacterString>
                </gmd:protocol>
                <gmd:name>
                  <gco:CharacterString>Google Earth KML 000014 poly and thumb</gco:CharacterString>
                </gmd:name>
                <gmd:description>
                  <gco:CharacterString>Google Earth KML poly thumb (requires Google Earth)</gco:CharacterString>
                </gmd:description>
              </gmd:CI_OnlineResource>
            </gmd:onLine>
            <gmd:onLine>
              <gmd:CI_OnlineResource>
                <gmd:linkage>
                  <gmd:URL>http://pandora.internal.govt:81/KML/wms-kml.php?SERVICE=000014&amp;LAYERS=AUST_2004.ECW</gmd:URL>
                </gmd:linkage>
                <gmd:protocol>
                  <gco:CharacterString>GLG:KML-2.0-http-get-map</gco:CharacterString>
                </gmd:protocol>
                <gmd:name>
                  <gco:CharacterString>Google Earth KML 000014 iws full resolution</gco:CharacterString>
                </gmd:name>
                <gmd:description>
                  <gco:CharacterString>Google Earth KML poly wms (requires Google Earth)</gco:CharacterString>
                </gmd:description>
              </gmd:CI_OnlineResource>
            </gmd:onLine>
            <gmd:onLine>
              <gmd:CI_OnlineResource>
                <gmd:linkage>
                  <gmd:URL>ecwp://pandora:81/iwsimages/aus/aust_2004.ecw</gmd:URL>
                </gmd:linkage>
                <gmd:protocol>
                  <gco:CharacterString>WWW:LINK-1.0-http- -samples</gco:CharacterString>
                </gmd:protocol>
                <gmd:name>
                  <gco:CharacterString>ECWP - Enhanced Compression Wavelet Protocol</gco:CharacterString>
                </gmd:name>
                <gmd:description>
                  <gco:CharacterString>ECWP - Streaming Imagery cut and paste to the open file dialog in ER Mapper or ER Mapper plugin for ArcGIS</gco:CharacterString>
                </gmd:description>
              </gmd:CI_OnlineResource>
            </gmd:onLine>
            <gmd:offLine>
              <gmd:MD_Medium>
                <gmd:name>
                  <gmd:MD_MediumNameCode codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_MediumNameCode"
                                         codeListValue="digitalLinearTap"/>
                </gmd:name>
                <gmd:mediumFormat>
                  <gmd:MD_MediumFormatCode codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_MediumFormatCode"
                                           codeListValue="tar"/>
                </gmd:mediumFormat>
                <gmd:mediumNote>
                  <gco:CharacterString>RSA000002</gco:CharacterString>
                </gmd:mediumNote>
              </gmd:MD_Medium>
            </gmd:offLine>
          </gmd:MD_DigitalTransferOptions>
        </gmd:transferOptions-->
      </gmd:MD_Distribution>
    </gmd:distributionInfo>
  </xsl:template><!--metadataExtensionInfo-->  
  <!--
  -->  
  <xsl:template name="dataQualityInfo">
      <gmd:dataQualityInfo>
        <gmd:DQ_DataQuality>
          <gmd:scope>
            <gmd:DQ_Scope>
              <gmd:level>
                <gmd:MD_ScopeCode>
                  <xsl:attribute name="codeList">http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_ScopeCode</xsl:attribute>
                  <xsl:attribute name="codeListValue">dataset</xsl:attribute>
                  <xsl:value-of select="'dataset'"/>
                </gmd:MD_ScopeCode>
              </gmd:level>
            </gmd:DQ_Scope>
          </gmd:scope>
          <gmd:report>
              <gmd:DQ_CompletenessOmission>
                <gmd:result>
                  <gmd:DQ_ConformanceResult>
                    <gmd:specification>
                      <xsl:call-template name="DummyCitation"/>
                    </gmd:specification>
                    <gmd:explanation>
                      <gco:CharacterString>COMPLETENESS</gco:CharacterString>
                    </gmd:explanation>
                    <gmd:pass>
                      <xsl:attribute name="gco:nilReason">missing</xsl:attribute>
                    </gmd:pass>
                  </gmd:DQ_ConformanceResult>
                </gmd:result>
              </gmd:DQ_CompletenessOmission>
          </gmd:report>
          <gmd:report>
            <gmd:DQ_AbsoluteExternalPositionalAccuracy>
              <gmd:result>
                <gmd:DQ_ConformanceResult>
                  <gmd:specification>
                    <xsl:call-template name="DummyCitation"/>
                  </gmd:specification>
                  <gmd:explanation>
                    <gco:CharacterString>POSITIONAL ACCURACY</gco:CharacterString>
                  </gmd:explanation>
                  <gmd:pass>
                    <xsl:attribute name="gco:nilReason">missing</xsl:attribute>
                  </gmd:pass>
                </gmd:DQ_ConformanceResult>
              </gmd:result>
            </gmd:DQ_AbsoluteExternalPositionalAccuracy>
          </gmd:report>
          <gmd:report>
            <gmd:DQ_ConceptualConsistency>
              <gmd:result>
                <gmd:DQ_ConformanceResult>
                  <gmd:specification>
                    <xsl:call-template name="DummyCitation"/>
                  </gmd:specification>
                  <gmd:explanation>
                    <gco:CharacterString>LOGICAL CONSISTENCY</gco:CharacterString>
                  </gmd:explanation>
                  <gmd:pass>
                    <xsl:attribute name="gco:nilReason">missing</xsl:attribute>
                  </gmd:pass>
                </gmd:DQ_ConformanceResult>
              </gmd:result>
            </gmd:DQ_ConceptualConsistency>
          </gmd:report>
          <gmd:report>
            <gmd:DQ_NonQuantitativeAttributeAccuracy>
              <gmd:result>
                <gmd:DQ_ConformanceResult>
                  <gmd:specification>
                    <xsl:call-template name="DummyCitation"/>
                  </gmd:specification>
                  <gmd:explanation>
                    <gco:CharacterString>ATTRIBUTE ACCURACY</gco:CharacterString>
                  </gmd:explanation>
                  <gmd:pass>
                    <xsl:attribute name="gco:nilReason">missing</xsl:attribute>
                  </gmd:pass>
                </gmd:DQ_ConformanceResult>
              </gmd:result>
            </gmd:DQ_NonQuantitativeAttributeAccuracy>
          </gmd:report>
          <gmd:lineage>
            <gmd:LI_Lineage>
              <gmd:statement>
                <gco:CharacterString>LINEAGE</gco:CharacterString>
              </gmd:statement>
              <xsl:variable name="tsteps">
                <xsl:element name="demcorrection"><xsl:value-of select="demcorrection"/></xsl:element>
                <xsl:element name="resampling"><xsl:value-of select="resampling"/></xsl:element>
              </xsl:variable>
              <xsl:call-template name="processStep">
                <xsl:with-param name="step" select="$step + 1"/>
                <xsl:with-param name="count" select="count($tsteps)"/>
                <xsl:with-param name="tsteps" select="$tsteps"/>
              </xsl:call-template>
            </gmd:LI_Lineage>
          </gmd:lineage>
        </gmd:DQ_DataQuality>
      </gmd:dataQualityInfo>
  </xsl:template><!--dataQualityInfo-->
  <xsl:template name="processStep">
    <xsl:param name="step" select="'1'"/>
    <xsl:param name="count" select="'1'"/>
    <xsl:param name="tsteps"/>
      <xsl:if test="$step &lt;= $count">
        <xsl:if test="normalize-space($tsteps[$step])">
          <processStep>
            <LI_ProcessStep>
              <xsl:attribute name="id"><xsl:value-of select="$step"/></xsl:attribute>
              <description>
                <gco:CharacterString>
                  <xsl:value-of select="local-name($tsteps[$step])"/>
                  <xsl:value-of select="normalize-space($tsteps[$step])"/>
                </gco:CharacterString>
              </description>
            </LI_ProcessStep>
          </processStep>
        </xsl:if>
        <xsl:call-template name="processStep">
          <xsl:with-param name="step" select="$step + 1"/>
          <xsl:with-param name="count" select="$count"/>
          <xsl:with-param name="tsteps" select="$tsteps"/>
        </xsl:call-template>
      </xsl:if>
  </xsl:template><!--processStep-->
  <!--
  -->  
  <xsl:template name="metadataConstraints">
    <gmd:metadataConstraints>
        <gmd:MD_LegalConstraints>
           <gmd:useLimitation>

              <gco:CharacterString>no limit</gco:CharacterString>
           </gmd:useLimitation>
           <gmd:accessConstraints>
              <gmd:MD_RestrictionCode codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_RestrictionCode"
                                      codeListValue="otherRestrictions"/>
           </gmd:accessConstraints>
           <gmd:useConstraints>
              <gmd:MD_RestrictionCode codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_RestrictionCode"
                                      codeListValue="otherRestrictions"/>
           </gmd:useConstraints>

           <gmd:otherConstraints>
              <gco:CharacterString>no constraints</gco:CharacterString>
           </gmd:otherConstraints>
        </gmd:MD_LegalConstraints>
    </gmd:metadataConstraints>
  </xsl:template>
 
  <!--
    S U B R O U T I N E S
  -->
  <xsl:template name="DummyCitation">
    <gmd:CI_Citation>
      <gmd:title>
        <xsl:attribute name="gco:nilReason">missing</xsl:attribute>
      </gmd:title>
      <xsl:call-template name="UnknownDate"/>
    </gmd:CI_Citation>
  </xsl:template><!-- /name="DummyCitation" -->
  <!--
  -->  
  <xsl:template name="UnknownDate">
    <gmd:date>
      <gmd:CI_Date>
        <gmd:date>
          <xsl:attribute name="gco:nilReason">unknown</xsl:attribute>
        </gmd:date>
        <gmd:dateType>
          <xsl:attribute name="gco:nilReason">unknown</xsl:attribute>
        </gmd:dateType>
      </gmd:CI_Date>
    </gmd:date>
  </xsl:template><!-- /name="UnknownDate" -->


  
</xsl:stylesheet>
