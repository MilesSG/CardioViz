import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE_URL = 'http://127.0.0.1:5000/api'

export const usePatientStore = defineStore('patient', {
  state: () => ({
    stats: {
      totalPatients: 0,
      highRiskPatients: 0,
      highRiskPercentage: 0
    },
    patients: [],
    selectedPatient: null,
    treatmentAnalysis: {},
    loading: false,
    error: null
  }),

  actions: {
    async fetchStats() {
      try {
        this.loading = true
        console.log('Fetching stats from:', `${API_BASE_URL}/stats`)
        const response = await axios.get(`${API_BASE_URL}/stats`)
        console.log('Stats response:', response.data)
        this.stats = {
          totalPatients: response.data.total_patients,
          highRiskPatients: response.data.high_risk_patients,
          highRiskPercentage: response.data.high_risk_percentage
        }
      } catch (error) {
        console.error('Error fetching stats:', error)
        this.error = error.message
      } finally {
        this.loading = false
      }
    },

    async fetchPatients() {
      try {
        this.loading = true
        console.log('Fetching patients from:', `${API_BASE_URL}/patients`)
        const response = await axios.get(`${API_BASE_URL}/patients`)
        console.log('Patients response:', response.data)
        this.patients = response.data
      } catch (error) {
        console.error('Error fetching patients:', error)
        this.error = error.message
      } finally {
        this.loading = false
      }
    },

    async fetchPatientVitals(patientId) {
      try {
        console.log(`Fetching vitals for patient ${patientId} from:`, `${API_BASE_URL}/patient/${patientId}/vitals`)
        const response = await axios.get(`${API_BASE_URL}/patient/${patientId}/vitals`)
        console.log('Vitals response:', response.data)
        return response.data
      } catch (error) {
        console.error('Error fetching patient vitals:', error)
        this.error = error.message
        return null
      }
    },

    async fetchTreatmentAnalysis() {
      try {
        this.loading = true
        console.log('Fetching treatment analysis from:', `${API_BASE_URL}/treatments/analysis`)
        const response = await axios.get(`${API_BASE_URL}/treatments/analysis`)
        console.log('Treatment analysis response:', response.data)
        this.treatmentAnalysis = response.data
      } catch (error) {
        console.error('Error fetching treatment analysis:', error)
        this.error = error.message
      } finally {
        this.loading = false
      }
    },

    setSelectedPatient(patient) {
      console.log('Setting selected patient:', patient)
      this.selectedPatient = patient
    }
  }
}) 