import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { mount } from '@vue/test-utils';
import { nextTick } from 'vue';
import NfcScanner from '../NfcScanner.vue';

// Mocking NDEFReader
let mockNdefReaderInstance;

describe('NfcScanner.vue', () => {
  beforeEach(() => {
    mockNdefReaderInstance = {
      scan: vi.fn().mockResolvedValue(undefined),
      addEventListener: vi.fn((event, handler) => {
        // Store listeners to be able to call them manually
        if (!mockNdefReaderInstance.listeners) mockNdefReaderInstance.listeners = {};
        if (!mockNdefReaderInstance.listeners[event]) mockNdefReaderInstance.listeners[event] = [];
        mockNdefReaderInstance.listeners[event].push(handler);
      }),
      removeEventListener: vi.fn(),
      // Basic dispatchEvent for testing 'readingerror'
      dispatchEvent: function(event) {
        if (this.listeners && this.listeners[event.type]) {
          this.listeners[event.type].forEach(handler => handler({ message: 'Simulated NFC Error' }));
        }
      }
    };
    window.NDEFReader = vi.fn(() => mockNdefReaderInstance);
    global.fetch = vi.fn(); // Mock global fetch
  });

  afterEach(() => {
    vi.restoreAllMocks(); // Clean up mocks
    delete window.NDEFReader;
    delete global.fetch;
    if (mockNdefReaderInstance.listeners) delete mockNdefReaderInstance.listeners;
  });

  it('handles successful scan and API unlock', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ name: 'Test Character', nfc_tag_id: 'test-serial', is_unlocked: true }),
    });

    const wrapper = mount(NfcScanner);
    await nextTick(); // Allow component to mount and NDEFReader to be set up

    // Simulate a successful NFC scan
    // Find the 'reading' event listener and call it
    const readingListenerCall = mockNdefReaderInstance.addEventListener.mock.calls.find(call => call[0] === 'reading');
    expect(readingListenerCall).toBeDefined();
    const readingHandler = readingListenerCall[1];

    await readingHandler({ serialNumber: 'test-serial' });
    await nextTick(); // Allow fetch and subsequent updates

    expect(global.fetch).toHaveBeenCalledWith('/api/unlock-character', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ serialNumber: 'test-serial' }),
    });

    expect(wrapper.vm.statusMessage).toBe('Successfully unlocked: Test Character!');
    expect(wrapper.emitted('scan-success')).toBeTruthy();
    expect(wrapper.emitted('scan-success')[0]).toEqual(['test-serial']);
    expect(wrapper.emitted('character-unlocked')).toBeTruthy();
    expect(wrapper.emitted('character-unlocked')[0][0]).toEqual({ name: 'Test Character', nfc_tag_id: 'test-serial', is_unlocked: true });
    expect(wrapper.emitted('close')).toBeTruthy();
  });

  it('handles scan with API error', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: false,
      status: 500,
      json: async () => ({ detail: 'Server Error' }),
    });

    const wrapper = mount(NfcScanner);
    await nextTick();

    const readingListenerCall = mockNdefReaderInstance.addEventListener.mock.calls.find(call => call[0] === 'reading');
    const readingHandler = readingListenerCall[1];
    await readingHandler({ serialNumber: 'test-api-error' });
    await nextTick();

    expect(global.fetch).toHaveBeenCalledWith('/api/unlock-character', expect.anything());
    expect(wrapper.vm.statusMessage).toBe('Failed to unlock character. Server said: Server Error');
    expect(wrapper.emitted('close')).toBeFalsy(); // Should not close on API error
  });

  it('handles scan with network error during fetch', async () => {
    global.fetch.mockRejectedValueOnce(new Error('Network failure'));

    const wrapper = mount(NfcScanner);
    await nextTick();

    const readingListenerCall = mockNdefReaderInstance.addEventListener.mock.calls.find(call => call[0] === 'reading');
    const readingHandler = readingListenerCall[1];
    await readingHandler({ serialNumber: 'test-network-error' });
    await nextTick();

    expect(wrapper.vm.statusMessage).toBe('Network error or problem making the request.');
    expect(wrapper.emitted('close')).toBeFalsy();
  });


  it('handles NFC readingerror event', async () => {
    const wrapper = mount(NfcScanner);
    await nextTick(); // Ensure component is mounted and listeners are attached

    // Simulate 'readingerror' event
    const errorListenerCall = mockNdefReaderInstance.addEventListener.mock.calls.find(call => call[0] === 'readingerror');
    expect(errorListenerCall).toBeDefined();
    const errorHandler = errorListenerCall[1];

    errorHandler(); // Call the error handler
    await nextTick();

    expect(wrapper.vm.statusMessage).toBe('Could not read the tag. Please try again.');
  });

  it('handles NDEFReader initial scan failing', async () => {
    // Override the global mock for this specific test case
    window.NDEFReader = vi.fn(() => ({
      scan: vi.fn().mockRejectedValue(new Error('NFC Scan Start Failed')),
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
    }));

    const wrapper = mount(NfcScanner);
    await nextTick(); // Allow mount and async scan attempt

    expect(wrapper.vm.statusMessage).toBe('Error: NFC Scan Start Failed');
  });

  it('handles WebNFC not supported', async () => {
    delete window.NDEFReader; // Ensure the property is removed for 'in' operator check

    const wrapper = mount(NfcScanner);
    await nextTick();

    expect(wrapper.vm.statusMessage).toBe('Web NFC is not supported on this device.');
  });
});
