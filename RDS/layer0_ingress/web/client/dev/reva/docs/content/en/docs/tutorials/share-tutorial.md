---
title: "OCM share functionality in Reva"
linkTitle: "OCM share functionality"
weight: 5
description: >
  OCM (Open Cloud Mesh) share functionality in Reva.
---

This is a guide on how to try the OCM share functionality in Reva in your local environment.

## Prerequisites
* golang
* make/automake
* git
* curl or wget

## 1. Clone the Reva repos
Clone the reva repo from https://github.com/cs3org/reva

```
git clone https://github.com/cs3org/reva
```

## 2. Build Reva
Follow the instructions in https://reva.link/docs/getting-started/install-reva/ for how to build reva. If you're making any local changes in reva, follow the "Build from sources" instructions.

## 3. Run Reva
Now we need to start two Reva daemons corresponding to two different mesh providers, thus enabling sharing of files between users belonging to these two providers. For our example,  we consider the example of CERNBox deployed at localhost:19000 and the CESNET owncloud at localhost:17000. Follow these steps:

```
cd examples/ocmd/ && mkdir -p /var/tmp/reva
../../cmd/revad/revad -c ocmd-server-1.toml & ../../cmd/revad/revad -c ocmd-server-2.toml &
```

This should start two Reva daemon (revad) services at the aforementioned endpoints.

## 4. Invitation Workflow
Before we start sharing files, we need to invite users belonging to different mesh providers so that file sharing can be initiated.
### 4.1 Generate invite token
Log in to reva as einstein at CERNBox

```
./cmd/reva/reva -insecure -host localhost:19000
>> login basic
login: einstein
password: relativity
OK
```

And generate an invite token:
```
>> ocm-invite-generate
status:<code:CODE_OK trace:"64a00a149f07ad5d7134b0eeb7c830f6" > invite_token:<token:"f9a25050-a0cf-4717-badb-b3574e3c0963" user_id:<idp:"cernbox.cern.ch" opaque_id:"4c510ada-c86b-4815-8820-42cdf82c3d51" > expiration:<seconds:1616847728 > >
```

Each token is valid for 24 hours from the time of creation.

### 4.2 Accept the token
Now a user on a different mesh provider needs to accept this token in order to initiate file sharing. So we need to call the corresponding endpoint as user marie at CESNET.

```
./cmd/reva/reva -insecure -host localhost:17000
>> login basic
login: marie
password: radioactivity
OK
```

And accept the invite token generated by einstein:
```
>> ocm-invite-forward -idp cernbox.cern.ch -token f9a25050-a0cf-4717-badb-b3574e3c0963
OK
```

## 5. Sharing functionality
Creating shares at the origin is specific to each vendor and would have different implementations across providers. Thus, to skip the OCS HTTP implementation provided with reva, we would directly make calls to the exposed GRPC Gateway services through the reva CLI.
### 5.1 Create a share on the original user's provider
#### 5.1.1 Create an example file
```
echo "Example file" > example.txt
```

#### 5.1.2 Log in to reva as einstein

```
./cmd/reva/reva -insecure -host localhost:19000
>> login basic
login: einstein
password: relativity
OK
```

#### 5.1.3 Upload the example.txt file
Create a folder and upload the file:

```
>> mkdir /home/my-folder
>> upload example.txt /home/my-folder/example.txt
Local file size: 15 bytes
Data server: http://localhost:19001/data/tus/d9360db0-3484-441a-8b7f-c9c0b8e63918
Allowed checksums: [type:RESOURCE_CHECKSUM_TYPE_MD5 priority:100  type:RESOURCE_CHECKSUM_TYPE_UNSET priority:1000 ]
Checksum selected: RESOURCE_CHECKSUM_TYPE_MD5
Local XS: RESOURCE_CHECKSUM_TYPE_MD5:085f396b2bdea443f3d5b889f84d49f5
File uploaded: 123e4567-e89b-12d3-a456-426655440000:fileid-einstein%2Fmy-folder%2Fexample.txt 15 /home/my-folder/example.txt
```

#### 5.1.4 Create the share
Call the ocm-share-create method with the required options. The user can list which all users have accepted the invite token and create shares using the retrieved info.
```
>> ocm-find-accepted-users
+--------------------------------------+-----------+-----------------+-------------+
| OPAQUEID                             | IDP       | MAIL            | DISPLAYNAME |
+--------------------------------------+-----------+-----------------+-------------+
| f7fbf8c8-139b-4376-b307-cf0a8c2d0d9c | cesnet.cz | marie@cesnet.cz | Marie Curie |
+--------------------------------------+-----------+-----------------+-------------+

>> ocm-share-create -grantee f7fbf8c8-139b-4376-b307-cf0a8c2d0d9c -idp cesnet.cz /home/my-folder
+--------------------------------------+-----------------+--------------------------------------+--------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------+-------------------+-------------+--------------------------------------+-------------------------------+-------------------------------+
| #                                    | OWNER.IDP       | OWNER.OPAQUEID                       | RESOURCEID                                                                                 | PERMISSIONS                                                                                                     | TYPE              | GRANTEE.IDP | GRANTEE.OPAQUEID                     | CREATED                       | UPDATED                       |
+--------------------------------------+-----------------+--------------------------------------+--------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------+-------------------+-------------+--------------------------------------+-------------------------------+-------------------------------+
| 23498b71-363e-4804-9f22-8c35dc070a06 | cernbox.cern.ch | 4c510ada-c86b-4815-8820-42cdf82c3d51 | storage_id:"123e4567-e89b-12d3-a456-426655440000" opaque_id:"fileid-einstein%2Fmy-folder"  | permissions:<get_path:true initiate_file_download:true list_container:true list_file_versions:true stat:true >  | GRANTEE_TYPE_USER | cesnet.cz   | f7fbf8c8-139b-4376-b307-cf0a8c2d0d9c | 2021-03-26 13:30:12 +0100 CET | 2021-03-26 13:30:12 +0100 CET |
+--------------------------------------+-----------------+--------------------------------------+--------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------+-------------------+-------------+--------------------------------------+-------------------------------+-------------------------------+

```
This would create a local share on einstein's mesh provider and call the unprotected endpoint `/ocm/shares` on the recipient's provider to create a remote share.

### 5.2 Accessing the share on the recipient's side
The recipient can access the list of shares shared with them. Similar to the create shares functionality, this implementation is specific to each vendor, so for the demo, we can access it through the reva CLI.

#### 5.2.1 Log in to reva as marie
```
./cmd/reva/reva -insecure -host localhost:17000
>> login basic
login: marie
password: radioactivity
OK
```

#### 5.2.2 Access the list of received shares
Call the ocm-share-list-received method.
```
>> ocm-share-list-received
+--------------------------------------+-----------------+--------------------------------------+--------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------+-------------+--------------------------------------+-------------------------------+-------------------------------+---------------------+
| #                                    | OWNER.IDP       | OWNER.OPAQUEID                       | RESOURCEID                                                                                 | PERMISSIONS                                                                                                                                                       | TYPE              | GRANTEE.IDP | GRANTEE.OPAQUEID                     | CREATED                       | UPDATED                       | STATE               |
+--------------------------------------+-----------------+--------------------------------------+--------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------+-------------+--------------------------------------+-------------------------------+-------------------------------+---------------------+
| 48bf1892-da3f-4e18-b9af-766595683689 | cernbox.cern.ch | 4c510ada-c86b-4815-8820-42cdf82c3d51 | storage_id:"123e4567-e89b-12d3-a456-426655440000" opaque_id:"fileid-einstein%2Fmy-folder"  | permissions:<get_path:true get_quota:true initiate_file_download:true list_grants:true list_container:true list_file_versions:true list_recycle:true stat:true >  | GRANTEE_TYPE_USER | cesnet.cz   | f7fbf8c8-139b-4376-b307-cf0a8c2d0d9c | 2021-03-26 13:30:12 +0100 CET | 2021-03-26 13:30:12 +0100 CET | SHARE_STATE_PENDING |
+--------------------------------------+-----------------+--------------------------------------+--------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------+-------------+--------------------------------------+-------------------------------+-------------------------------+---------------------+
```