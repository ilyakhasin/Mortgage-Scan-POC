import React, { useState, useRef } from 'react';
import {
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  ActivityIndicator,
  ScrollView,
  Alert,
} from 'react-native';
import { Camera, CameraType } from 'expo-camera';
import * as FileSystem from 'expo-file-system';
import { uploadDocument, mapFields } from './src/veryfiClient';

export default function App() {
  const [hasPermission, setHasPermission] = useState(null);
  const [showCamera, setShowCamera] = useState(false);
  const [processing, setProcessing] = useState(false);
  const [extractedFields, setExtractedFields] = useState([]);
  const cameraRef = useRef(null);

  const requestCameraPermission = async () => {
    const { status } = await Camera.requestCameraPermissionsAsync();
    setHasPermission(status === 'granted');
    if (status === 'granted') {
      setShowCamera(true);
    } else {
      Alert.alert('Permission Denied', 'Camera permission is required to scan documents.');
    }
  };

  const takePicture = async () => {
    if (!cameraRef.current) return;

    try {
      setProcessing(true);
      setShowCamera(false);

      // Capture photo
      const photo = await cameraRef.current.takePictureAsync({
        quality: 0.8,
        base64: true,
      });

      // Upload to Veryfi
      const response = await uploadDocument(photo.base64);

      // Map fields
      const fields = mapFields(response);
      setExtractedFields(fields);

      Alert.alert('Success', 'Document processed successfully!');
    } catch (error) {
      console.error('Error processing document:', error);
      Alert.alert(
        'Error',
        error.message || 'Failed to process document. Please try again.'
      );
      setExtractedFields([]);
    } finally {
      setProcessing(false);
    }
  };

  const renderCameraView = () => (
    <View style={styles.container}>
      <Camera
        style={styles.camera}
        type={CameraType.back}
        ref={cameraRef}
      >
        <View style={styles.cameraControls}>
          <TouchableOpacity
            style={styles.captureButton}
            onPress={takePicture}
          >
            <Text style={styles.captureButtonText}>Capture</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={styles.cancelButton}
            onPress={() => setShowCamera(false)}
          >
            <Text style={styles.cancelButtonText}>Cancel</Text>
          </TouchableOpacity>
        </View>
      </Camera>
    </View>
  );

  const renderMainView = () => (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Mortgage Scan POC</Text>
        <Text style={styles.subtitle}>Veryfi OCR Integration</Text>
      </View>

      <TouchableOpacity
        style={styles.takePictureButton}
        onPress={requestCameraPermission}
        disabled={processing}
      >
        <Text style={styles.takePictureButtonText}>
          {processing ? 'Processing...' : 'Take Picture'}
        </Text>
      </TouchableOpacity>

      {processing && (
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#007AFF" />
          <Text style={styles.loadingText}>Processing document...</Text>
        </View>
      )}

      {extractedFields.length > 0 && (
        <View style={styles.resultsContainer}>
          <Text style={styles.resultsTitle}>Extracted Fields</Text>
          <View style={styles.table}>
            {extractedFields.map((field, index) => (
              <View
                key={index}
                style={[
                  styles.tableRow,
                  index % 2 === 0 ? styles.tableRowEven : styles.tableRowOdd,
                ]}
              >
                <Text style={styles.tableLabel}>{field.label}</Text>
                <Text style={styles.tableValue}>{field.value}</Text>
              </View>
            ))}
          </View>
        </View>
      )}
    </ScrollView>
  );

  if (showCamera) {
    return renderCameraView();
  }

  return renderMainView();
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    padding: 20,
    paddingTop: 60,
    backgroundColor: '#fff',
    alignItems: 'center',
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
  },
  subtitle: {
    fontSize: 14,
    color: '#666',
    marginTop: 5,
  },
  takePictureButton: {
    backgroundColor: '#007AFF',
    margin: 20,
    padding: 20,
    borderRadius: 10,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  takePictureButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
  camera: {
    flex: 1,
  },
  cameraControls: {
    flex: 1,
    backgroundColor: 'transparent',
    flexDirection: 'column',
    justifyContent: 'flex-end',
    padding: 20,
  },
  captureButton: {
    backgroundColor: '#007AFF',
    padding: 20,
    borderRadius: 10,
    alignItems: 'center',
    marginBottom: 10,
  },
  captureButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
  cancelButton: {
    backgroundColor: '#FF3B30',
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
  },
  cancelButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  loadingContainer: {
    padding: 20,
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 10,
    fontSize: 16,
    color: '#666',
  },
  resultsContainer: {
    margin: 20,
    backgroundColor: '#fff',
    borderRadius: 10,
    padding: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
    elevation: 3,
  },
  resultsTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 15,
  },
  table: {
    borderWidth: 1,
    borderColor: '#e0e0e0',
    borderRadius: 5,
    overflow: 'hidden',
  },
  tableRow: {
    flexDirection: 'row',
    padding: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  tableRowEven: {
    backgroundColor: '#f9f9f9',
  },
  tableRowOdd: {
    backgroundColor: '#fff',
  },
  tableLabel: {
    flex: 1,
    fontSize: 14,
    fontWeight: '600',
    color: '#333',
  },
  tableValue: {
    flex: 1,
    fontSize: 14,
    color: '#666',
    textAlign: 'right',
  },
});
